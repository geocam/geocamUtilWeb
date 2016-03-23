# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import json

from django import template
from django.conf import settings
from geocamUtil.datetimeJsonEncoder import DatetimeJsonEncoder

register = template.Library()

@register.filter(name="json_dumps")
def json_dumps(value):
    return json.dumps(value, cls=DatetimeJsonEncoder)
