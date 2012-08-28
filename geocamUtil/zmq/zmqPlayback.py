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

from geocamUtil.zmq.util import zmqLoop, LogParser
from geocamUtil.zmq.publisher import ZmqPublisher


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
        self.logFile = open(self.logPath, 'rb')
        self.log = LogParser(self.logFile)
        i = 0
        for rec in self.log:
            topicMatch = False
            if self.opts.topic:
                for topic in self.opts.topic:
                    if rec.msg.startswith(topic):
                        topicMatch = True
                        break
            else:
                topicMatch = True

            if topicMatch:
                self.publisher.pubStream.send(rec.msg)
                if i % 100 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                i += 1
        print
        print 'message count:', i


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <zmqCentral-messages-xxx.txt>')
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
