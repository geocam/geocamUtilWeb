#!/usr/bin/env python

import logging

from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil.zmq.publisher import ZmqPublisher
from geocamUtil.zmq.util import zmqLoop

TEST_MESSAGE = open('exampleMessageWithAttachment.txt', 'rb').read()


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
