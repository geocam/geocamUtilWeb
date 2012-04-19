#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import logging

from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil.zmq.util import zmqLoop
from geocamUtil.zmq.subscriber import ZmqSubscriber
from geocamUtil import anyjson as json

prettyPrintG = False

def handleMessage(topic, body):
    if prettyPrintG:
        print topic
        print json.dumps(body, sort_keys=True, indent=4)
    else:
        print '%s: %s' % (topic, json.dumps(body))


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <prefix>')
    parser.add_option('-p', '--pretty',
                      action='store_true', default=False,
                      help='Pretty-print JSON objects')
    ZmqSubscriber.addOptions(parser, 'testSubscriber')
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error('expected exactly 1 arg')
    logging.basicConfig(level=logging.DEBUG)

    # set up networking
    s = ZmqSubscriber(**ZmqSubscriber.getOptionValues(opts))
    s.start()

    # subscribe to the message we want
    global prettyPrintG
    prettyPrintG = opts.pretty
    s.subscribe(args[0], handleMessage)

    zmqLoop()


if __name__ == '__main__':
    main()
