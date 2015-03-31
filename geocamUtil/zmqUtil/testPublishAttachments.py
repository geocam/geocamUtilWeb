#!/usr/bin/env python
# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import os
import logging

from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil.zmqUtil.publisher import ZmqPublisher
from geocamUtil.zmqUtil.util import zmqLoop

thisDir = os.path.dirname(__file__)
TEST_MESSAGE = open(os.path.join(thisDir, 'exampleMessageWithAttachment.txt'), 'rb').read()


def pubMessage(p):
    topic = 'dds.Resolve.RESOLVE_CAM_ProcessedImage'
    body = TEST_MESSAGE
    logging.debug('publishing: %s:%s', topic, body)
    p.sendRaw(topic, body)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog')
    ZmqPublisher.addOptions(parser, 'testPublishAttachments')
    opts, args = parser.parse_args()
    if args:
        parser.error('expected no args')
    logging.basicConfig(level=logging.DEBUG)

    # set up networking
    p = ZmqPublisher(**ZmqPublisher.getOptionValues(opts))
    p.start()

    # start publishing an arbitrary message that central should forward
    pubTimer = ioloop.PeriodicCallback(lambda: pubMessage(p), 1000)
    pubTimer.start()

    zmqLoop()


if __name__ == '__main__':
    main()
