# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.conf import settings as djangoSettings


def static(request):
    """
    Backport django.core.context_processors.static to Django 1.2.
    """
    return {'STATIC_URL': djangoSettings.STATIC_URL}


def settings(request):
    return {'settings': djangoSettings}
