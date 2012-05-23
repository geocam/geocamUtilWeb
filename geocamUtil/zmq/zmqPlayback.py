#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys
import logging

from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil.zmq.util import zmqLoop
from geocamUtil.zmq.publisher import ZmqPublisher
from geocamUtil import anyjson as json


class ZmqPlayback(object):
    def __init__(self, logPath, opts):
        self.logPath = logPath
        self.opts = opts
        self.publisher = ZmqPublisher(**ZmqPublisher.getOptionValues(opts))
        print 'topics:', self.opts.topic

    def start(self):
        self.publisher.start()

        # the delay gives a chance to connect to central before publishing
        self.publishTimer = ioloop.DelayedCallback(self.playLog, 100)
        self.publishTimer.start()

    def playLog(self):
        self.log = open(self.logPath, 'rb')
        i = 0
        for line in self.log:
            try:
                sentinel, timestamp, msgSizeStr, msg = line.split(' ', 3)
                msgSize = int(msgSizeStr)
            except ValueError:
                print 'warning: bad log line parse:'
                print line
                continue
            msg = msg[:-1]  # chop newline
            if sentinel != '@@@':
                print 'warning: bad sentinel'
                print line
                continue
            if len(msg) != msgSize:
                print 'warning: bad message length %d != %d' % (len(msg), msgSize)
                print line
                continue

            topicMatch = False
            if self.opts.topic:
                for topic in self.opts.topic:
                    if msg.startswith(topic):
                        topicMatch = True
                        break
            else:
                topicMatch = True

            if topicMatch:
                self.publisher.pubStream.send(msg)
                if i % 100 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                i += 1
        print
        print 'message count:', i


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <zmqCentral-messages-xxx.txt>')
    #parser.add_option('-s', '--speedup',
    #                  type='int', default=1,
    #                  help='Speedup factor [%default]')
    #parser.add_option('--max',
    #                  action='store_true', default=False,
    #                  help='Override speedup, play back messages as fast as possible')
    parser.add_option('-t', '--topic',
                      action='append',
                      help='Only print specified topics, can specify multiple times')
    ZmqPublisher.addOptions(parser, 'zmqPlayback')
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error('expected exactly 1 arg')
    logging.basicConfig(level=logging.DEBUG)

    pb = ZmqPlayback(args[0], opts)
    pb.start()

    zmqLoop()

if __name__ == '__main__':
    main()
