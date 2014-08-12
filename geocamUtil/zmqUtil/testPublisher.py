#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import logging
import sys

import zmq
from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil.zmqUtil.publisher import ZmqPublisher
from geocamUtil.zmqUtil.util import zmqLoop


def pubMessage(publisher, line):
    topic, body = line.split(':', 1)
    logging.debug('publishing: %s:%s', topic, body)
    publisher.sendRaw(topic, body)


def stdinHandler(publisher):
    line = sys.stdin.readline()[:-1]
    topic, body = line.split(':', 1)
    logging.debug('publishing: %s:%s', topic, body)
    publisher.sendRaw(topic, body)


def main():
    import optparse
    parser = optparse.OptionParser('usage: testLineSource.py testMessages.txt | %prog')
    ZmqPublisher.addOptions(parser, 'testPublisher')
    opts, args = parser.parse_args()
    if args:
        parser.error('expected no args')
    logging.basicConfig(level=logging.DEBUG)

    # set up networking
    publisher = ZmqPublisher(**ZmqPublisher.getOptionValues(opts))
    publisher.start()

    ioloop.IOLoop.instance().add_handler(sys.stdin.fileno(),
                                         lambda fd, events: stdinHandler(publisher),
                                         ioloop.IOLoop.READ)
    zmqLoop()


if __name__ == '__main__':
    main()
