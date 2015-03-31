#!/usr/bin/env python
# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

"""
The filePublisher script receives files published by filePublisher over
0MQ, and writes them to disk.

In case there are multiple instances of filePublisher running, you can
specify which one you want to listen to by matching its --subtopic
argument.

To reduce bandwidth, use the --timestampSpacing option to specify the
minimum timestamp between files to send from the same file source. For
example, if we know files are written approximately every 5 seconds, and
we want to only receive every second file (about one every 10 seconds),
we can set --timestampSpacing=8. After sending one file, the file 5
seconds later will be ignored because it is less than 8 seconds later,
but the following file will be sent. We use --timestampSpacing=8 instead
of --timestampSpacing=10 so as to not miss files in case they are
written just a bit early (timing jitter in the periodic file source).

(Each --watchXxx argument to filePublisher counts as a separate "file
source" for the purposes of the --timestampSpacing argument.)

In the common case that the files are images, we can tell filePublisher
to apply various processing steps that may reduce the bandwidth:

  --imageCrop: Crop the image. Format: "<width>x<height>+<xmin>+<ymin>".
               Example: --imageCrop="100x100+300+400".

  --imageResize: Subsample the image. Format:
                 "<width>x<height>". Example: --imageResize="640x480".

  --imageFormat: Convert the image to the specified format. Example: "jpg".

When multiple image processing operations are specified, they are
applied in the order listed above.

The filename of the file sent by filePublisher is automatically
annotated to reflect the processing operations that were applied to it. For example:

 "foo.png" -> "foo_crop_100_100_300_400_resize_50_50.jpg"

filePublisher will apply the --imageXxx processing steps to files that
appear to be images based on their extension. Examples: ".jpg",
".png". Other files will be passed through unmodified.
"""

import logging
import os
import base64
import traceback

from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil.zmqUtil.publisher import ZmqPublisher
from geocamUtil.zmqUtil.subscriber import ZmqSubscriber
from geocamUtil.zmqUtil.util import zmqLoop


def parseImageResize(imageResize):
    width, height = imageResize.split('x', 1)
    return {
        'width': int(width),
        'height': int(height)
    }


def parseImageCrop(imageCrop):
    widthHeight, x, y = imageCrop.split('+', 2)
    width, height = widthHeight.split('x', 1)
    return {
        'width': int(width),
        'height': int(height),
        'x': int(x),
        'y': int(y)
    }


class FileReceiver(object):
    def __init__(self, opts):
        self.request = {
            'timeout': opts.timeout,
            'pollPeriod': opts.pollPeriod,
        }
        if opts.timestampSpacing:
            self.request['timestampSpacing'] = opts.timestampSpacing
        if opts.imageResize:
            self.request['imageResize'] = parseImageResize(opts.imageResize)
        if opts.imageCrop:
            self.request['imageCrop'] = parseImageCrop(opts.imageCrop)
        if opts.imageFormat:
            self.request['imageFormat'] = opts.imageFormat

        self.outputDirectory = opts.output
        self.subtopic = opts.subtopic
        self.noRequest = opts.noRequest

        opts.moduleName = opts.moduleName.format(subtopic=opts.subtopic)
        self.publisher = ZmqPublisher(**ZmqPublisher.getOptionValues(opts))
        self.subscriber = ZmqSubscriber(**ZmqSubscriber.getOptionValues(opts))

        self.requestPeriod = 0.5 * opts.timeout

    def getTopic(self, msgType):
        return 'geocamUtil.filePublisher.%s.%s' % (self.subtopic, msgType)

    def start(self):
        self.publisher.start()
        self.subscriber.start()

        self.subscriber.subscribeJson(self.getTopic('file'),
                                      self.handleFile)
        self.subscriber.subscribeRaw(self.getTopic('response'),
                                     self.handleResponse)

        if not self.noRequest:
            self.sendRequest()
            requestTimer = ioloop.PeriodicCallback(self.sendRequest,
                                                   self.requestPeriod * 1000)
            requestTimer.start()

    def sendRequest(self):
        logging.debug('sendRequest')
        self.publisher.sendJson(self.getTopic('request'),
                                self.request)

    def handleResponse(self, topic, msg):
        logging.debug('received response: %s', repr(msg))
        # nothing to do

    def handleFile(self, topic, msg):
        try:
            self.handleFile0(topic, msg)
        except:  # pylint: disable=W0702
            logging.warning('%s', traceback.format_exc())

    def handleFile0(self, topic, msg):
        f = msg['file']
        outputPath = os.path.join(self.outputDirectory, f['filename'])
        _fmt, data = f['contents'].split(':', 1)
        contents = base64.b64decode(data)
        file(outputPath, 'w').write(contents)
        logging.debug('wrote %s bytes to %s', len(contents), outputPath)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog OPTIONS\n' + __doc__)
    parser.add_option('-o', '--output',
                      default='.',
                      help='Directory to write received files to [%default]')
    parser.add_option('-p', '--pollPeriod',
                      type='float', default=1.0,
                      help='Period between checks for a new latest file (seconds) [%default]')
    parser.add_option('-s', '--timestampSpacing',
                      type='float', default=5.0,
                      help='Ignore latest file unless it is this much newer than the last file sent (seconds) [%default]')
    parser.add_option('--timeout',
                      type='float', default=30.0,
                      help='Keep publishing files for this long after each request from fileReceiver (seconds) [%default]')
    parser.add_option('-r', '--imageResize',
                      help='Subsample any images to specified size (e.g. "640x480")')
    parser.add_option('-c', '--imageCrop',
                      help='Crop any images to specified size and location (e.g. "100x100+300+400")')
    parser.add_option('-f', '--imageFormat',
                      help='Output any images in the specified format (e.g. "jpg")')
    parser.add_option('-t', '--subtopic',
                      default='standard',
                      help='Subtopic to use when receiving zmq message [%default]')
    parser.add_option('-n', '--noRequest',
                      action='store_true', default=False,
                      help='Do not request any files from filePublisher, but write any files that are received, for example because they are requested by other receivers. May be useful for debugging.')
    ZmqPublisher.addOptions(parser, 'fileReceiver.{subtopic}')
    ZmqSubscriber.addOptions(parser, 'fileReceiver.{subtopic}')
    opts, args = parser.parse_args()
    if args:
        parser.error('expected no args')

    logging.basicConfig(level=logging.DEBUG)

    p = FileReceiver(opts)
    p.start()
    zmqLoop()


if __name__ == '__main__':
    main()
