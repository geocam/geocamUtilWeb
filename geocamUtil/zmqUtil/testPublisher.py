#!/usr/bin/env python
# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import logging
import sys

from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil.zmqUtil.publisher import ZmqPublisher
from geocamUtil.zmqUtil.util import zmqLoop


def stdinHandler(publisher):
    line = sys.stdin.readline()
    if not line:
        # EOF... end program
        ioloop.IOLoop.instance().stop()
        return
    line = line[:-1]
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
