# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import json
from django import template
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe

from geocamUtil.models import SiteFrame
from geocamUtil.forms.SelectSiteFrameForm import SelectSiteFrameForm

register = template.Library()

@register.simple_tag(name='siteframes_dict')
def siteframes_dict():
    siteframes = SiteFrame.objects.all().order_by('name')
    result = {}
    for siteframe in siteframes:
        result[siteframe.id] = model_to_dict(siteframe)
    return mark_safe(json.dumps(result))


@register.simple_tag(name='siteframe')
def siteframe(id):
    try:
        siteframe = SiteFrame.objects.get(pk=id)
        return mark_safe(json.dumps(model_to_dict(siteframe)))
    except:
        return None


@register.simple_tag(name='siteframe_form')
def siteframe_form():
    if SiteFrame.objects.count() > 1:
        theForm =  SelectSiteFrameForm()
        return theForm.as_table()
    return ''
