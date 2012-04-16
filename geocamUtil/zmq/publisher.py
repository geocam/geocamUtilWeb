#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import logging
import re

import zmq
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop

from geocamUtil import anyjson as json
from geocamUtil.zmq.util import getTimestamp, parseEndpoint, DEFAULT_CENTRAL_RPC_PORT

PUBLISHER_OPT_DEFAULTS = {'moduleName': None,
                          'centralRpcEndpoint': 'tcp://127.0.0.1:%s' % DEFAULT_CENTRAL_RPC_PORT,
                          'publishEndpoint': 'tcp://127.0.0.1:random',
                          'heartbeatPeriodMsecs': 5000}


class ZmqPublisher(object):
    def __init__(self,
                 moduleName=None,
                 context=None,
                 centralRpcEndpoint=PUBLISHER_OPT_DEFAULTS['centralRpcEndpoint'],
                 publishEndpoint=PUBLISHER_OPT_DEFAULTS['publishEndpoint'],
                 heartbeatPeriodMsecs=PUBLISHER_OPT_DEFAULTS['heartbeatPeriodMsecs']):
        self.moduleName = moduleName

        if context is None:
            context = zmq.Context()
        self.context = context

        self.centralRpcEndpoint = parseEndpoint(centralRpcEndpoint,
                                                defaultPort=DEFAULT_CENTRAL_RPC_PORT)
        self.publishEndpoint = parseEndpoint(publishEndpoint,
                                             defaultPort='random')
        self.heartbeatPeriodMsecs = heartbeatPeriodMsecs

        self.reqStream = None
        self.pubStream = None
        self.heartbeatTimer = None
        self.counter = 0

    @classmethod
    def addOptions(cls, parser, defaultModuleName):
        if not parser.has_option('--moduleName'):
            parser.add_option('--moduleName',
                              default=defaultModuleName,
                              help='Name to use for this module [%default]')
        if not parser.has_option('--centralRpcEndpoint'):
            parser.add_option('--centralRpcEndpoint',
                              default=PUBLISHER_OPT_DEFAULTS['centralRpcEndpoint'],
                              help='Endpoint where central listens for RPC calls [%default]')
        if not parser.has_option('--publishEndpoint'):
            parser.add_option('--publishEndpoint',
                              default=PUBLISHER_OPT_DEFAULTS['publishEndpoint'],
                              help='Endpoint to publish messages on [%default]')
        if not parser.has_option('--heartbeatPeriodMsecs'):
            parser.add_option('--heartbeatPeriodMsecs',
                              default=PUBLISHER_OPT_DEFAULTS['heartbeatPeriodMsecs'],
                              type='int',
                              help='Period for sending heartbeats to central [%default]')

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
        msg = json.dumps({'method': 'heartbeat',
                          'id': self.counter,
                          'params': [{'moduleName': self.moduleName,
                                      'timestamp': getTimestamp(),
                                      'pub': self.publishEndpoint}]})
        self.reqStream.send(msg)
        self.counter += 1

    def handleHeartbeatAck(self, messages):
        for msg in messages:
            logging.debug('ZmqPublisher: heartbeatAck %s', msg)

    def send(self, topic, obj):
        self.pubStream.send('%s:%s' % (topic, json.dumps(obj)))

    def start(self):
        reqSocket = self.context.socket(zmq.REQ)
        self.reqStream = ZMQStream(reqSocket)
        self.reqStream.connect(self.centralRpcEndpoint)
        self.reqStream.on_recv(self.handleHeartbeatAck)

        pubSocket = self.context.socket(zmq.PUB)
        self.pubStream = ZMQStream(pubSocket)

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
