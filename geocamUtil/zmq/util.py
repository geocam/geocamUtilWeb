#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import re


def parseEndpoint(endpoint, defaultPort=None):
    if '://' in endpoint:
        return endpoint
    if re.match('\d+', endpoint):
        return 'tcp://127.0.0.1:%d' % endpoint
    m = re.match('([\w\.]+):(\d+)', endpoint)
    if m:
        host = m.group(1)
        port = m.group(2)
        return 'tcp://%s:%d' % (host, port)
    if defaultPort is not None:
        m = re.match('[\w\.]+', endpoint)
        if m:
            return 'tcp://%s:%d' % (endpoint, defaultPort)
    raise ValueError('endpoint format "%s" not supported' % endpoint)
