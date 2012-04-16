# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import zmq
from zmq.eventloop.zmqstream import ZMQStream

from zmq.eventloop import ioloop

from geocamUtil import anyjson as json


class ZmqSubscriber(object):
    def __init__(self, sock):
        self.sock = sock
        self.handlers = {}
        self.stream = ZMQStream(self.sock)
        self.stream.on_recv(self.routeMessage)

    def routeMessage(self, messages):
        for msg in messages:
            topic, body = msg.split(':', 1)
            obj = json.loads(body)
            topicRegistry = self.handlers[topic]
            for handler in topicRegistry.itervalues():
                handler(topic, obj)

    def subscribe(self, topic, handler, handlerId=None):
        topicRegistry = self.handlers.setdefault(topic, {})
        if handlerId is None:
            handlerId = len(topicRegistry)
        if not topicRegistry:
            self.sock.setsockopt(zmq.SUBSCRIBE, topic + ':')
        topicRegistry[handlerId] = handler

    def unsubscribe(self, topic, handlerId):
        topicRegistry = self.handlers[topic]
        del topicRegistry[handlerId]
        if not topicRegistry:
            self.sock.setsockopt(zmq.UNSUBSCRIBE, topic + ':')


def zmqLoop():
    ioloop.IOLoop.instance().start()
