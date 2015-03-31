#!/usr/bin/env python
# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import re
import time
import platform
import datetime
import email.parser

from zmq.eventloop import ioloop

DEFAULT_CENTRAL_RPC_PORT = 7814
DEFAULT_CENTRAL_SUBSCRIBE_PORT = 7815
DEFAULT_CENTRAL_PUBLISH_PORT = 7816


def getTimestamp(posixTime=None):
    if posixTime is None:
        posixTime = time.time()
    return int(posixTime * 1000000)


def getTimestampFields(timestampStr):
    """
    Used to convert from JSON-over-0MQ microseconds-since-epoch
    timestamp representation (used by ddsZmqBridge and some of our other
    utilities) to a two-part timestamp representation as used by many of
    our Django models.
    """
    timestampFull = int(timestampStr)
    timestampSeconds = datetime.datetime.utcfromtimestamp(timestampFull / 1000000)
    timestampMicroseconds = timestampFull % 1000000
    return timestampSeconds, timestampMicroseconds


def getShortHostName():
    node = platform.node()
    return node.split('.', 1)[0]


def parseEndpoint(endpoint,
                  defaultPort=None,
                  defaultHost='127.0.0.1',
                  defaultProto='tcp://',
                  centralHost='127.0.0.1'):
    # substitute centralHost into template, if needed
    endpoint = re.sub(r'\{centralHost\}', centralHost, endpoint)

    # fully qualified endpoint in the form "tcp://host:port"
    if '://' in endpoint:
        return endpoint

    # endpoint in the form "host:port"
    if re.match(r'^([\w\.]+):(random|\d+)$', endpoint):
        return '%s%s' % (defaultProto, endpoint)

    # endpoint in the form "host"
    if re.match(r'^[\w\.]+$', endpoint):
        if defaultPort is None:
            raise ValueError('endpoint format %s has no port' % endpoint)
        else:
            return '%s%s:%s' % (defaultProto, endpoint, defaultPort)

    # endpoint in the form ":port"
    if re.match(r'^:(random|\d+)$', endpoint):
        return '%s%s%s' % (defaultProto, defaultHost, endpoint)

    raise ValueError('can\'t resolve endpoint format "%s"' % endpoint)


def hasAttachments(msg):
    colonIndex = msg.find(':')
    ctype = ':Content-Type: '
    return msg[colonIndex:(colonIndex + len(ctype))] == ctype


def parseMessageBody(body):
    if body.startswith('Content-Type:'):
        msg = email.parser.Parser().parsestr(body)
        assert msg.is_multipart()
        jsonSection = msg.get_payload()[0]
        attachments = msg.get_payload()[1:]

        if attachments:
            # parser quirk: remove last section if it's blank
            lastSectionText = attachments[-1].get_payload()
            if isinstance(lastSectionText, basestring) and re.match(r'^\s*$', lastSectionText):
                attachments.pop()

        return {'json': jsonSection.get_payload(), 'attachments': attachments}
    else:
        return {'json': body, 'attachments': []}


def parseMessage(msg):
    topic, body = msg.split(':', 1)
    parsed = parseMessageBody(body)
    parsed['topic'] = topic
    return parsed


def zmqLoop():
    ioloop.IOLoop.instance().start()


class LogRecord(object):
    def __init__(self, timestamp, attachmentsPath, msg):
        self.timestamp = timestamp
        self.attachmentsPath = attachmentsPath
        self.msg = msg

    def writeTo(self, stream):
        stream.write('@@@ %d %d %s ' % (self.timestamp, len(self.msg), self.attachmentsPath))
        stream.write(self.msg)
        stream.write('\n')


class LogParser(object):
    def __init__(self, logFile):
        self.logFile = logFile

    def __iter__(self):
        for lineNum, line in enumerate(self.logFile):
            try:
                sentinel, timestampStr, msgSizeStr, attachmentsPath, msg = line.split(' ', 4)
                timestamp = int(timestampStr)
                msgSize = int(msgSizeStr)
            except ValueError:
                print 'warning: bad log line parse in line %d' % (lineNum + 1)
                print line
                continue
            msg = msg[:-1]  # chop newline
            if sentinel != '@@@':
                print 'warning: bad sentinel in line %d' % (lineNum + 1)
                print line
                continue
            if len(msg) != msgSize:
                print 'warning: bad message length %d != %d in line %d' % (len(msg), msgSize, lineNum + 1)
                print line
                continue
            if attachmentsPath != '-':
                print 'warning: zmqPlayback can not handle attachments in line %d' % (lineNum + 1)
                print line
                continue

            yield LogRecord(timestamp, attachmentsPath, msg)
