#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
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
                  defaultProto='tcp://'):
    # tcp://host:port
    if '://' in endpoint:
        return endpoint

    # host:port
    if re.match(r'^([\w\.]+):(random|\d+)$', endpoint):
        return '%s%s' % (defaultProto, endpoint)

    # host
    if re.match(r'^[\w\.]+$', endpoint):
        if defaultPort is None:
            raise ValueError('endpoint format %s has no port' % endpoint)
        else:
            return '%s%s:%s' % (defaultProto, endpoint, defaultPort)

    # :port
    if re.match(r'^:(random|\d+)$', endpoint):
        return '%s%s%s' % (defaultProto, defaultHost, endpoint)

    raise ValueError('can\'t resolve endpoint format "%s"' % endpoint)


def hasAttachments(msg):
    colonIndex = msg.find(':')
    ctype = ':Content-Type: '
    return msg[colonIndex : (colonIndex + len(ctype))] == ctype

def parseMessageBody(body):
    if body.startswith('Content-Type:'):
        msg = email.parser.Parser().parsestr(body)
        assert msg.is_multipart()
        jsonSection = msg.get_payload()[0]
        attachments = msg.get_payload()[1:]

        if attachments:
            # parser quirk: remove last section if it's blank
            lastSectionText = attachments[-1].get_payload()
            if isinstance(lastSectionText, basestring) and re.match('^\s*$', lastSectionText):
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
