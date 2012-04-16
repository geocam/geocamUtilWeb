#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys
import os
import logging
import datetime
import time
import traceback
import atexit

import zmq
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil import anyjson as json

THIS_MODULE = 'zmqCentral'
DEFAULT_KEEPALIVE_MS = 10000


def getTimestamp():
    return int(time.time() * 1000)


class ZmqCentral(object):
    def __init__(self, opts):
        self.opts = opts

        self.info = {}
        self.subStreams = {}
        self.rpcStream = None
        self.pubStream = None

    def subscribeIfNeeded(self, moduleName, modulePublishEndpoint):
        if moduleName in self.subStreams:
            oldPublishEndpoint, _oldStream = self.subStreams[moduleName]
            if oldPublishEndpoint == modulePublishEndpoint:
                # already connected, nothing to do
                return False
            else:
                # must disconnect before connecting to new publish endpoint
                self.unsubModule(moduleName)
        logging.info('subscribing to messages from %s on endpoint %s',
                     moduleName, modulePublishEndpoint)
        stream = ZMQStream(self.context.socket(zmq.SUB))
        stream.connect(modulePublishEndpoint)
        stream.setsockopt(zmq.SUBSCRIBE, '')
        stream.on_recv(lambda messages: self.handleMessages(moduleName, messages))
        self.subStreams[moduleName] = (modulePublishEndpoint, stream)
        return True

    def publishAndLog(self, moduleName, msg):
        timestamp = getTimestamp()
        self.pubStream.send(msg)
        self.messageLog.write('@@@ %s %d %d\n' % (moduleName, timestamp, len(msg)))
        self.messageLog.write(msg)
        self.messageLog.write('\n')

    def handleHeartbeat(self, params):
        moduleName = params['moduleName']
        now = getTimestamp()
        params['centralTimestamp'] = now
        if moduleName not in self.info:
            logging.debug('module %s connected', moduleName)
            self.publishAndLog(THIS_MODULE, 'central.connect.%s:' % moduleName
                               + json.dumps({'timestamp': now}))
        self.info[moduleName] = params
        config = params.get('config', None)
        if config:
            endpoints = config.get('pub', None)
            if endpoints:
                endpoint = endpoints[0]
                self.subscribeIfNeeded(moduleName, endpoint)
            keepalive = config.get('keepalive', DEFAULT_KEEPALIVE_MS)
        else:
            keepalive = DEFAULT_KEEPALIVE_MS
        self.publishAndLog(THIS_MODULE, 'central.heartbeat.%s:' % moduleName
                           + json.dumps(params))
        params['timeout'] = now + keepalive
        return 'ok'

    def handleInfo(self, params):
        return self.info

    def handleMessages(self, moduleName, messages):
        for msg in messages:
            self.publishAndLog(moduleName, msg)

    def handleRpcCall(self, messages):
        for msg in messages:
            try:
                call = json.loads(msg)
                callId = call['id']
            except:  # pylint: disable=W0702
                self.rpcStream.send(json.dumps({'result': None,
                                                'error': 'malformed request'}))

            try:
                method = call['method']
                params = call['params']
                if method == 'heartbeat':
                    result = self.handleHeartbeat(*params)
                elif method == 'info':
                    result = self.handleInfo(*params)
                else:
                    raise ValueError('unknown method %s' % method)
                self.rpcStream.send(json.dumps({'result': result,
                                                'error': None,
                                                'id': callId}))
            except:  # pylint: disable=W0702
                errClass, errObject, errTB = sys.exc_info()[:3]
                errText = '%s.%s: %s' % (errClass.__module__,
                                         errClass.__name__,
                                         str(errObject))
                logging.debug(''.join(traceback.format_tb(errTB)))
                logging.debug(errText)
                self.rpcStream.send(json.dumps({'result': None,
                                                'error': errText,
                                                'id': callId}))

    def unsubModule(self, moduleName):
        if moduleName in self.subStreams:
            moduleEndpoint, stream = self.subStreams.pop(moduleName)
            logging.info('unsubscribing from module %s on %s',
                         moduleName, moduleEndpoint)
            stream.close()

    def handleDisconnectTimer(self):
        now = getTimestamp()
        disconnectModules = []
        for moduleName, entry in self.info.iteritems():
            timeout = entry.get('timeout', None)
            if timeout is not None and now > timeout:
                disconnectModules.append(moduleName)
        for moduleName in disconnectModules:
            logging.info('module %s disconnected', moduleName)
            self.publishAndLog(THIS_MODULE, 'central.disconnect.%s:' % moduleName
                               + json.dumps({'timestamp': now}))
            self.unsubModule(moduleName)
            del self.info[moduleName]

    def readyLog(self, pathTemplate, timestamp):
        if '%s' in pathTemplate:
            timeText = timestamp.strftime('%Y-%m-%d-%H-%M-%S')
            logFile = pathTemplate % timeText
        else:
            logFile = pathTemplate
        if not os.path.exists(self.logDir):
            os.makedirs(self.logDir)
        logPath = os.path.join(self.logDir, logFile)
        if '%s' in pathTemplate:
            latestPath = os.path.join(self.logDir, pathTemplate % 'latest')
            if os.path.islink(latestPath):
                os.unlink(latestPath)
        os.symlink(logFile, latestPath)
        return logPath

    def start(self):
        # open log files
        now = datetime.datetime.utcnow()
        self.logDir = os.path.abspath(self.opts.logDir)
        self.messageLogPath = self.readyLog(self.opts.messageLog, now)
        self.messageLog = open(self.messageLogPath, 'a')
        self.consoleLogPath = self.readyLog(self.opts.consoleLog, now)

        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(self.consoleLogPath)
        fh.setLevel(logging.DEBUG)
        rootLogger.addHandler(fh)
        if self.opts.foreground:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            rootLogger.addHandler(ch)

        # daemonize
        if self.opts.foreground:
            logging.info('staying in foreground')
        else:
            logging.info('daemonizing')
            pid = os.fork()
            if pid != 0:
                os._exit(0)
            os.setsid()
            pid = os.fork()
            if pid != 0:
                os._exit(0)
            os.chdir('/')
            os.close(1)
            os.close(2)
            nullFd = os.open('/dev/null', os.O_RDWR)
            os.dup2(nullFd, 1)
            os.dup2(nullFd, 2)

        # set up zmq
        self.context = zmq.Context()
        self.rpcStream = ZMQStream(self.context.socket(zmq.REP))
        self.rpcStream.bind(self.opts.rpcEndpoint)
        self.rpcStream.on_recv(self.handleRpcCall)
        self.pubStream = ZMQStream(self.context.socket(zmq.PUB))
        self.pubStream.bind(self.opts.publishEndpoint)
        for entry in self.opts.subscribeEndpoint:
            moduleName, endpoint = entry.split('@')
            self.subscribeIfNeeded(moduleName, endpoint)

        self.disconnectTimer = ioloop.PeriodicCallback(self.handleDisconnectTimer, 5000)
        self.disconnectTimer.start()

    def shutdown(self):
        self.messageLog.flush()


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog')
    parser.add_option('-r', '--rpcEndpoint',
                      default='tcp://127.0.0.1:7814',
                      help='Endpoint to listen on for RPC requests [%default]')
    parser.add_option('-p', '--publishEndpoint',
                      default='tcp://127.0.0.1:7815',
                      help='Endpoint for publishing messages [%default]')
    parser.add_option('-s', '--subscribeEndpoint',
                      default=[],
                      action='append',
                      help='Non-central-aware publisher to subscribe to (format "moduleName@endpoint"; can specify multiple times)')
    parser.add_option('-d', '--logDir',
                      default='log',
                      help='Directory to place logs in [%default]')
    parser.add_option('-m', '--messageLog',
                      default='zmqCentral-messages-%s.txt',
                      help='Log file for message traffic [%default]')
    parser.add_option('-c', '--consoleLog',
                      default='zmqCentral-console-%s.txt',
                      help='Log file for debugging zmqCentral [%default]')
    parser.add_option('-f', '--foreground',
                      action='store_true', default=False,
                      help='Do not daemonize zmqCentral on startup')
    opts, args = parser.parse_args()
    if args:
        parser.error('expected no args')
    zc = ZmqCentral(opts)
    zc.start()
    atexit.register(zc.shutdown)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
