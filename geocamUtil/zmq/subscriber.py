# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import zmq
from zmq.eventloop.zmqstream import ZMQStream

from django.core import serializers

from geocamUtil import anyjson as json
from geocamUtil.zmq.util import parseEndpoint, DEFAULT_CENTRAL_PUBLISH_PORT
from geocamUtil.models.ExtrasDotField import convertToDotDictRecurse

SUBSCRIBER_OPT_DEFAULTS = {'moduleName': None,
                           'centralPublishEndpoint': 'tcp://127.0.0.1:%d'
                           % DEFAULT_CENTRAL_PUBLISH_PORT}


class ZmqSubscriber(object):
    def __init__(self,
                 moduleName,
                 context=None,
                 centralPublishEndpoint=SUBSCRIBER_OPT_DEFAULTS['centralPublishEndpoint']):
        self.moduleName = moduleName

        if context is None:
            context = zmq.Context.instance()
        self.context = context

        self.centralPublishEndpoint = parseEndpoint(centralPublishEndpoint,
                                                    defaultPort=DEFAULT_CENTRAL_PUBLISH_PORT)

        self.handlers = {}
        self.counter = 0
        self.deserializer = serializers.get_deserializer('json')

    @classmethod
    def addOptions(cls, parser, defaultModuleName):
        if not parser.has_option('--moduleName'):
            parser.add_option('--moduleName',
                              default=defaultModuleName,
                              help='Name to use for this module [%default]')
        if not parser.has_option('--centralPublishEndpoint'):
            parser.add_option('--centralPublishEndpoint',
                              default=SUBSCRIBER_OPT_DEFAULTS['centralPublishEndpoint'],
                              help='Endpoint where central publishes messages [%default]')

    @classmethod
    def getOptionValues(cls, opts):
        result = {}
        for key in SUBSCRIBER_OPT_DEFAULTS.iterkeys():
            val = getattr(opts, key, None)
            if val is not None:
                result[key] = val
        return result

    def start(self):
        sock = self.context.socket(zmq.SUB)
        self.stream = ZMQStream(sock)
        self.stream.setsockopt(zmq.IDENTITY, self.moduleName)
        self.stream.connect(self.centralPublishEndpoint)
        self.stream.on_recv(self.routeMessage)

    def routeMessage(self, messages):
        for msg in messages:
            colonIndex = msg.find(':')
            topic = msg[:(colonIndex + 1)]
            body = msg[(colonIndex + 1):]

            for topicPrefix, registry in self.handlers.iteritems():
                if topic.startswith(topicPrefix):
                    topicRegistry = registry
                    break

            for handler in topicRegistry.itervalues():
                handler(topic[:-1], body)

    def subscribeRaw(self, topicPrefix, handler):
        topicRegistry = self.handlers.setdefault(topicPrefix, {})
        if not topicRegistry:
            self.stream.setsockopt(zmq.SUBSCRIBE, topicPrefix)
        handlerId = (topicPrefix, self.counter)
        topicRegistry[self.counter] = handler
        self.counter += 1
        return handlerId

    def subscribeJson(self, topicPrefix, handler):
        def jsonHandler(topicPrefix, body):
            return handler(topicPrefix, convertToDotDictRecurse(json.loads(body)))
        return self.subscribeRaw(topicPrefix, jsonHandler)

    def subscribeDjango(self, topicPrefix, handler):
        def djangoHandler(topicPrefix, body):
            obj = json.loads(body)
            dataText = json.dumps([obj['data']])
            modelInstance = list(self.deserializer(dataText))[0]
            return handler(topicPrefix, modelInstance.object)
        return self.subscribeRaw(topicPrefix, djangoHandler)

    def unsubscribe(self, handlerId):
        topicPrefix, index = handlerId
        topicRegistry = self.handlers[topicPrefix]
        del topicRegistry[index]
        if not topicRegistry:
            self.stream.setsockopt(zmq.UNSUBSCRIBE, topicPrefix)

    def connect(self, endpoint):
        self.stream.connect(endpoint)
