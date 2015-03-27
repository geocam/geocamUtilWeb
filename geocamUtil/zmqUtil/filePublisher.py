#!/usr/bin/env python
# __BEGIN_LICENSE__
#Copyright © 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
#
#The xGDS platform is licensed under the Apache License, Version 2.0 
#(the "License"); you may not use this file except in compliance with the License. 
#You may obtain a copy of the License at 
#http://www.apache.org/licenses/LICENSE-2.0.
#
#Unless required by applicable law or agreed to in writing, software distributed 
#under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
#CONDITIONS OF ANY KIND, either express or implied. See the License for the 
#specific language governing permissions and limitations under the License.
# __END_LICENSE__

"""
The filePublisher script publishes the latest file in a streaming set of
files over 0MQ.  It is designed to minimize latency. Old files are never
published (to sync all files in batch mode, you can use existing tools
such as 'rsync').

You can control what new files filePublisher watches for with the
following flags:

  --watchFilePattern: Files matching the specified UNIX glob, like
                      "somedir/*.jpg"

  --watchDirectory: Files in the specified directory

  --watchSymlink: Files pointed to by the specified symlink. This
                  assumes a cooperative file writer that updates a
                  symlink whenever it writes a new file. Checking a
                  symlink may be more efficient than the other
                  approaches in the common case that the new files are
                  appearing in a directory containing thousands of
                  files.

You can use the flags together, and each can be specified multiple times
to watch for a variety of files.

You can run multiple instances of filePublisher at the same time. If you
want to receive them with separate receivers, you can use the --subtopic
argument to, in effect, put the publishers on different channels. Then
run the matching fileReceiver.py with the same --subtopic argument.

Many parameters used by filePublisher (polling rates, how often to send
files, etc) are specified as arguments to the fileReceiver script that
receives the files.
"""

# pylint: disable=W0201

import logging
import glob
import os
import time
import json
import base64
import tempfile
import traceback

from zmq.eventloop import ioloop
ioloop.install()

import PIL.Image

from geocamUtil.zmqUtil.publisher import ZmqPublisher
from geocamUtil.zmqUtil.subscriber import ZmqSubscriber
from geocamUtil.zmqUtil.util import zmqLoop


def getFileDict(filePath, fileMtime):
    return {
        'type': 'PlainFile',
        'mtime': fileMtime,
        'filename': os.path.basename(filePath),
        'contents': 'base64:' + base64.b64encode(open(filePath, 'r').read())
    }


class FileSource(object):
    def __init__(self):
        self.lastFileSent = None
        self.lastFileSentMtime = None

    def isFileNew(self, candidatePath, candidateFileMtime, timestampSpacing):
        if self.lastFileSent is not None and candidatePath == self.lastFileSent:
            return False
        if self.lastFileSentMtime is not None and timestampSpacing is not None and (candidateFileMtime - self.lastFileSentMtime) < timestampSpacing:
            return False
        return True

    def checkForNewFileAndRemember(self, timestampSpacing):
        candidatePath = self.getCandidateFile()
        if candidatePath is None:
            return None

        candidateFileMtime = os.path.getmtime(candidatePath)
        if self.isFileNew(candidatePath, candidateFileMtime, timestampSpacing):
            self.lastFileSent = candidatePath
            self.lastFileSentMtime = candidateFileMtime
            return (candidatePath, candidateFileMtime)
        else:
            return None

    def getCandidateFile(self):
        raise NotImplementedError()


class PatternFileSource(FileSource):
    def __init__(self, pattern):
        super(PatternFileSource, self).__init__()
        self.pattern = pattern
        self.knownFiles = {}

    def getCandidateFile(self):
        files = glob.glob(self.pattern)
        newFiles = [f for f in files
                    if f not in self.knownFiles]
        if newFiles:
            self.knownFiles = dict.fromkeys(files)
            newestFile = max(newFiles,
                             key=os.path.getmtime)
            return newestFile

        return None


class DirectoryFileSource(PatternFileSource):
    def __init__(self, path):
        super(DirectoryFileSource, self).__init__(os.path.join(path, '*'))


class SymlinkFileSource(FileSource):
    def __init__(self, path):
        super(SymlinkFileSource, self).__init__()
        self.path = path

    def getCandidateFile(self):
        return os.readlink(self.path)


class ImageProcessor(object):
    def __init__(self, resize, crop, fmt, tmpDir):
        self.crop = crop
        self.resize = resize
        self.fmt = fmt
        self.tmpDir = tmpDir

    def isImage(self, path):
        _name, ext = os.path.splitext(path)
        return (ext in ('.jpg', '.jpeg', '.png', '.tif', '.tiff'))

    def processImage(self, path):
        bname = os.path.basename(path)
        name, ext = os.path.splitext(bname)
        if self.crop:
            name += ('_crop_%s_%s_%s_%s' %
                     (self.crop['width'],
                      self.crop['height'],
                      self.crop['x'],
                      self.crop['y']))
        if self.resize:
            name += ('_resize_%s_%s' %
                     (self.resize['width'],
                      self.resize['height']))
        if self.fmt:
            ext = '.' + self.fmt
        outputPath = os.path.join(self.tmpDir, name + ext)

        img = PIL.Image.open(path)
        if self.crop:
            img = img.crop((self.crop['x'],
                            self.crop['y'],
                            self.crop['x'] + self.crop['width'],
                            self.crop['y'] + self.crop['height']))
        if self.resize:
            img = img.resize((self.resize['width'],
                              self.resize['height']),
                             PIL.Image.ANTIALIAS)
        img.save(outputPath)
        return outputPath


class FilePublisher(object):
    def __init__(self, opts):
        self.sources = ([PatternFileSource(x) for x in opts.watchFilePattern] +
                        [DirectoryFileSource(x) for x in opts.watchDirectory] +
                        [SymlinkFileSource(x) for x in opts.watchSymlink])

        self.subtopic = opts.subtopic

        self.pollTimer = None
        self.stopPollingTime = None
        self.imageProcessor = None
        self.tmpDir = tempfile.mkdtemp(prefix='filePublisher')

        opts.moduleName = opts.moduleName.format(subtopic=opts.subtopic)
        self.publisher = ZmqPublisher(**ZmqPublisher.getOptionValues(opts))
        self.subscriber = ZmqSubscriber(**ZmqSubscriber.getOptionValues(opts))

    def getTopic(self, msgType):
        return 'geocamUtil.filePublisher.%s.%s' % (self.subtopic, msgType)

    def start(self):
        self.publisher.start()
        self.subscriber.start()
        self.subscriber.subscribeJson(self.getTopic('request'),
                                      self.handleRequest)

    def handleRequest(self, topic, requestDict):
        logging.debug('handleRequest %s', json.dumps(requestDict))
        self.requestTimeout = requestDict['timeout']
        self.pollPeriod = requestDict['pollPeriod']
        self.timestampSpacing = requestDict.get('timestampSpacing')
        if 'imageResize' in requestDict or 'imageCrop' in requestDict or 'imageFormat' in requestDict:
            self.imageProcessor = ImageProcessor(resize=requestDict.get('imageResize'),
                                                 crop=requestDict.get('imageCrop'),
                                                 fmt=requestDict.get('imageFormat'),
                                                 tmpDir=self.tmpDir)
        else:
            self.imageProcessor = None

        self.stopPollingTime = time.time() + self.requestTimeout

        self.publisher.sendRaw(self.getTopic('response'), 'ok')

        if self.pollTimer:
            self.pollTimer.stop()
            self.pollTimer = None
        self.pollTimer = ioloop.PeriodicCallback(self.pollHandler,
                                                 self.pollPeriod * 1000)
        self.pollTimer.start()

    def pollHandler(self):
        try:
            self.pollHandler0()
        except:  # pylint: disable=W0702
            logging.warning('%s', traceback.format_exc())

    def pollHandler0(self):
        logging.debug('pollHandler')

        if time.time() > self.stopPollingTime:
            logging.info('request timed out, stopping polling')
            self.pollTimer.stop()
            self.pollTimer = None

        for source in self.sources:
            newFileInfo = source.checkForNewFileAndRemember(self.timestampSpacing)
            if newFileInfo:
                self.publishFile(newFileInfo)

    def publishFile(self, fileInfo):
        path, mtime = fileInfo
        if self.imageProcessor and self.imageProcessor.isImage(path):
            processedPath = self.imageProcessor.processImage(path)
            logging.debug('sending %s', processedPath)
            self.publisher.sendJson(self.getTopic('file'),
                                    {'file': getFileDict(processedPath, mtime)})
            os.unlink(processedPath)
        else:
            logging.debug('sending %s', path)
            self.publisher.sendJson(self.getTopic('file'),
                                    {'file': getFileDict(path, mtime)})


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog OPTIONS\n' + __doc__)
    parser.add_option('-f', '--watchFilePattern',
                      action='append', default=[],
                      help='Watch for files matching the specified UNIX glob, like "somedir/*.jpg"')
    parser.add_option('-d', '--watchDirectory',
                      action='append', default=[],
                      help='Watch for files in the specified directory')
    parser.add_option('-s', '--watchSymlink',
                      action='append', default=[],
                      help='Watch for files pointed to by the specified symlink. This assumes a cooperative file writer that updates a symlink whenever it writes a new file. This may be more efficient than the other approaches when new files are appearing in a directory containing many files.')
    parser.add_option('-t', '--subtopic',
                      default='standard',
                      help='Subtopic to use when publishing zmq message [%default]')
    ZmqPublisher.addOptions(parser, 'filePublisher.{subtopic}')
    ZmqSubscriber.addOptions(parser, 'filePublisher.{subtopic}')
    opts, args = parser.parse_args()
    if args:
        parser.error('expected no args')

    logging.basicConfig(level=logging.DEBUG)

    p = FilePublisher(opts)
    p.start()
    zmqLoop()


if __name__ == '__main__':
    main()
