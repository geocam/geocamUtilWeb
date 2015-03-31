# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.conf import settings as djangoSettings


def static(request):
    """
    Backport django.core.context_processors.static to Django 1.2.
    """
    return {'STATIC_URL': djangoSettings.STATIC_URL}


def settings(request):
    return {'settings': djangoSettings}
