# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django import template
from django.conf import settings

from geocamUtil import TimeUtil

register = template.Library()


@register.filter(name="utc_to_django")
def utc_to_django(value):
    return TimeUtil.utcToTimeZone(value, settings.TIME_ZONE)
