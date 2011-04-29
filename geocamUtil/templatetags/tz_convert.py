
from django import template
from django.conf import settings

from geocamUtil import TimeUtil

register = template.Library()

@register.filter(name="utc_to_django")
def utc_to_django(value):
    return TimeUtil.utcToTimeZone(value, settings.TIME_ZONE)
