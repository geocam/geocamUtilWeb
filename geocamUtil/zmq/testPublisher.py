#!/usr/bin/env python

import logging

import zmq
from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil.zmq.zmqPublisher import ZmqPublisher

PUBLISH_PORT = 'tcp://127.0.0.1:8750'


def pubMessage(sock, msg):
    logging.debug('publishing: %s', msg)
    sock.send(msg)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog')
    _opts, args = parser.parse_args()
    if args:
        parser.error('expected no args')
    logging.basicConfig(level=logging.DEBUG)

    # initialize publish socket
    context = zmq.Context()
    h = ZmqPublisher(context, 'testPublisher', {'pub': [PUBLISH_PORT]})
    h.start()

    # start publishing an arbitrary message that central should forward
    sock = context.socket(zmq.PUB)
    sock.bind(PUBLISH_PORT)
    pubTimer = ioloop.PeriodicCallback(lambda: pubMessage(sock, 'hello'), 1000)
    pubTimer.start()

    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
