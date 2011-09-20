# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import time
import rfc822

import django.views.static


def staticServeWithExpires(request, path, document_root=None, show_indexes=False,
                           expireSeconds=365 * 24 * 60 * 60):
    response = django.views.static.serve(request, path, document_root, show_indexes)
    response['Expires'] = rfc822.formatdate(time.time() + expireSeconds)
    return response
