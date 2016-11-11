# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
#
#The xGDS platform is licensed under the Apache License, Version 2.0 
#(the "License"); you may not use this file except in compliance with the License. 
#You may obtain a copy of the License at 
#http://www.apache.org/licenses/LICENSE-2.0.
#
#Unless required by applicable law or agreed to in writing, software distributed 
#under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
#CONDITIONS OF ANY KIND, either express or implied. See the License for the 
#specific language governing permissions and limitations under the License.
# __END_LICENSE__

import pytz
from django.utils.functional import lazy
from django import forms
from django.forms.models import ChoiceField
from geocamUtil.models import SiteFrame
from django.core.cache import caches
from django.conf import settings

def getTimezoneChoices(empty=None):
    _cache = caches['default']
    TIMEZONE_CHOICES = _cache.get('TIMEZONE_CHOICES')
    if not TIMEZONE_CHOICES:
        try:
            siteframe_zones = SiteFrame.objects.values('timezone').distinct()
            listresult = sorted([str(r['timezone']) for r in siteframe_zones])
            TIMEZONE_CHOICES = [(v, v) for v in listresult]
            TIMEZONE_CHOICES.append(('utc', 'UTC'))
            _cache.set('TIMEZONE_CHOICES',TIMEZONE_CHOICES)
        except:
            return [] # just to handle the case where we are migrating and have not yet built this table
    if empty:
        TIMEZONE_CHOICES.insert(0, (None, '-------'))
    return TIMEZONE_CHOICES


class AbstractImportForm(forms.Form):
    timezone = ChoiceField(required=True, choices=lazy(getTimezoneChoices, list)(), initial=settings.TIME_ZONE)

    def getTimezone(self):
        if self.cleaned_data['timezone'] == 'utc':
            tz = pytz.utc
        else:
            tz = pytz.timezone(self.cleaned_data['timezone'])
        return tz

    def getTimezoneName(self):
        if self.cleaned_data['timezone'] == 'utc':
            return 'Etc/UTC'
        else:
            return self.cleaned_data['timezone']
        return None

    class meta:
        abstract=True
    
    
