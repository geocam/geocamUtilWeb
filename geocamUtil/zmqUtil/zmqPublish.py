#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

"""
Accepts line-oriented <topic>:<content> messages on stdin and publishes
them through the zmqCentral hub.
"""

import logging
import sys

from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil.zmqUtil.publisher import ZmqPublisher
from geocamUtil.zmqUtil.util import zmqLoop


def pubMessage(prefix, p):
    line = sys.stdin.readline()
    if not line:
        raise RuntimeError('EOF')
    line = line[:-1]
    logging.debug('publishing: %s', prefix + line)
    p.pubStream.send(prefix + line)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog')
    ZmqPublisher.addOptions(parser, 'zmqPublish')
    parser.add_option('-p', '--prefix',
                      default='',
                      help='Prefix to prepend to incoming lines before publishing them (DO include trailing "." if you want it)')
    opts, args = parser.parse_args()
    if args:
        parser.error('expected no args')
    logging.basicConfig(level=logging.DEBUG)

    # set up networking
    p = ZmqPublisher(**ZmqPublisher.getOptionValues(opts))
    p.start()

    # start publishing an arbitrary message that central should forward
    pubTimer = ioloop.PeriodicCallback(lambda: pubMessage(opts.prefix, p), 0.1)
    pubTimer.start()

    zmqLoop()


if __name__ == '__main__':
    main()
