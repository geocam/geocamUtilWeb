#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import logging
import time

import zmq
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop

from geocamUtil import anyjson as json
from geocamUtil.zmq.util import parseEndpoint

DEFAULT_CENTRAL_RPC_ENDPOINT = 'tcp://127.0.0.1:7814'



def addPublisherOptions(parser):
    parser.add_option('--moduleName',
                      help='Name to use for this module')
    parser.add_option('--centralRpcEndpoint',
                      default=DEFAULT_CENTRAL_RPC_ENDPOINT,
                      help='Endpoint to use for RPC calls to central [%default]')
    parser.add_option('--publishEndpoint',
                      default='random',
                      help='Endpoint to publish messages on [%default]')
    parser.add_option('--heartbeatPeriodMsecs',
                      default=5000, type='int',
                      help='Period for sending heartbeats to central [%default]'))


class ZmqPublisher(object):
    def __init__(self,
                 moduleName,
                 ioloop=None,
                 context=None,
                 publishEndpoint=None,
                 centralRpcEndpoint='tcp://127.0.0.1:7814',
                 heartbeatPeriodMsecs=5000):
        if ioloop is None:
            from zmq.eventloop import ioloop
            ioloop.install()
        self.ioloop = ioloop

        if context is None:
            context = zmq.Context()
        self.context = context

        self.moduleName = moduleName
        self.centralRpcEndpoint = parseEndpoint(centralRpcEndpoint)
        self.periodMilliseconds = periodMilliseconds
        if config is None:
            config = {}
        self.config = config

        self.reqSocket = None
        self.reqStream = None
        self.heartbeatTimer = None
        self.counter = 0

    def heartbeat(self):
        logging.debug('ZmqPublisher: heartbeat')
        msg = json.dumps({'method': 'heartbeat',
                          'id': self.counter,
                          'params': [{'moduleName': self.moduleName,
                                      'timestamp': int(time.time() * 1000),
                                      'config': self.config}]})
        self.reqSocket.send(msg)
        self.counter += 1

    def handleHeartbeatAck(self, messages):
        for msg in messages:
            logging.debug('ZmqPublisher: heartbeatAck %s', msg)

    def start(self):
        self.reqSocket = self.context.socket(zmq.REQ)
        self.reqSocket.connect(self.centralRpcEndpoint)
        self.reqStream = ZMQStream(self.reqSocket)
        self.reqStream.on_recv(self.handleHeartbeatAck)
        self.heartbeatTimer = ioloop.PeriodicCallback(self.heartbeat,
                                                      self.periodMilliseconds)
        self.heartbeatTimer.start()
        self.heartbeat()
