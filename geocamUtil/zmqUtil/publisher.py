#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

# pylint: disable=E1101

import logging
import re

import zmq
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop

from django.core import serializers

from geocamUtil import anyjson as json
from geocamUtil.zmqUtil.util import (getTimestamp,
                                     parseEndpoint,
                                     getShortHostName,
                                     DEFAULT_CENTRAL_SUBSCRIBE_PORT)

PUBLISHER_OPT_DEFAULTS = {'moduleName': None,
                          'centralSubscribeEndpoint': 'tcp://127.0.0.1:%s'
                          % DEFAULT_CENTRAL_SUBSCRIBE_PORT,
                          'publishEndpoint': 'tcp://127.0.0.1:random',
                          'heartbeatPeriodMsecs': 5000,
                          # 'highWaterMark': 100
                          }


class ZmqPublisher(object):
    def __init__(self,
                 moduleName,
                 context=None,
                 centralSubscribeEndpoint=PUBLISHER_OPT_DEFAULTS['centralSubscribeEndpoint'],
                 publishEndpoint=PUBLISHER_OPT_DEFAULTS['publishEndpoint'],
                 heartbeatPeriodMsecs=PUBLISHER_OPT_DEFAULTS['heartbeatPeriodMsecs'],
                 # highWaterMark=PUBLISHER_OPT_DEFAULTS['highWaterMark']
                 ):
        self.moduleName = moduleName

        if context is None:
            context = zmq.Context.instance()
        self.context = context

        self.centralSubscribeEndpoint = parseEndpoint(centralSubscribeEndpoint,
                                                      defaultPort=DEFAULT_CENTRAL_SUBSCRIBE_PORT)
        self.publishEndpoint = parseEndpoint(publishEndpoint,
                                             defaultPort='random')
        self.heartbeatPeriodMsecs = heartbeatPeriodMsecs
        #self.highWaterMark = highWaterMark

        self.pubStream = None
        self.heartbeatTimer = None

        self.serializer = serializers.get_serializer('json')()

    @classmethod
    def addOptions(cls, parser, defaultModuleName):
        if not parser.has_option('--moduleName'):
            parser.add_option('--moduleName',
                              default=defaultModuleName,
                              help='Name to use for this module [%default]')
        if not parser.has_option('--centralSubscribeEndpoint'):
            parser.add_option('--centralSubcribeEndpoint',
                              default=PUBLISHER_OPT_DEFAULTS['centralSubscribeEndpoint'],
                              help='Endpoint where central listens for messages [%default]')
        if not parser.has_option('--publishEndpoint'):
            parser.add_option('--publishEndpoint',
                              default=PUBLISHER_OPT_DEFAULTS['publishEndpoint'],
                              help='Endpoint to publish messages on [%default]')
        if not parser.has_option('--heartbeatPeriodMsecs'):
            parser.add_option('--heartbeatPeriodMsecs',
                              default=PUBLISHER_OPT_DEFAULTS['heartbeatPeriodMsecs'],
                              type='int',
                              help='Period for sending heartbeats to central [%default]')
        #if not parser.has_option('--highWaterMark'):
        #    parser.add_option('--highWaterMark',
        #                      default=PUBLISHER_OPT_DEFAULTS['highWaterMark'],
        #                      type='int',
        #                      help='High-water mark for publish socket (see 0MQ docs) [%default]')

    @classmethod
    def getOptionValues(cls, opts):
        result = {}
        for key in PUBLISHER_OPT_DEFAULTS.iterkeys():
            val = getattr(opts, key, None)
            if val is not None:
                result[key] = val
        return result

    def heartbeat(self):
        logging.debug('ZmqPublisher: heartbeat')
        self.sendJson('central.heartbeat.%s' % self.moduleName,
                      {'host': getShortHostName(),
                       'pub': self.publishEndpoint})

    def sendRaw(self, topic, body):
        self.pubStream.send('%s:%s' % (topic, body))

    def sendJson(self, topic, obj):
        if isinstance(obj, dict):
            obj.setdefault('module', self.moduleName)
            obj.setdefault('timestamp', str(getTimestamp()))
        self.sendRaw(topic, json.dumps(obj))

    def sendDjango(self, modelInstance, topic=None, topicSuffix=None):
        dataText = self.serializer.serialize([modelInstance])
        data = json.loads(dataText)[0]
        if topic is None:
            topic = data['model'].encode('utf-8')
            if topicSuffix is not None:
                topic += topicSuffix
        self.sendJson(topic, {'data': data})

    def start(self):
        pubSocket = self.context.socket(zmq.PUB)
        self.pubStream = ZMQStream(pubSocket)
        # self.pubStream.setsockopt(zmq.IDENTITY, self.moduleName)
        # self.pubStream.setsockopt(zmq.HWM, self.highWaterMark)
        self.pubStream.connect(self.centralSubscribeEndpoint)

        if self.publishEndpoint.endswith(':random'):
            endpointWithoutPort = re.sub(r':random$', '', self.publishEndpoint)
            port = self.pubStream.bind_to_random_port(endpointWithoutPort)
            self.publishEndpoint = '%s:%d' % (endpointWithoutPort, port)
        else:
            self.pubStream.bind(self.publishEndpoint)

        self.heartbeatTimer = ioloop.PeriodicCallback(self.heartbeat,
                                                      self.heartbeatPeriodMsecs)
        self.heartbeatTimer.start()
        self.heartbeat()
