# __BEGIN_LICENSE__
# Copyright (c) 2015, United States Government, as represented by the 
# Administrator of the National Aeronautics and Space Administration. 
# All rights reserved.
#
# The xGDS platform is licensed under the Apache License, Version 2.0 
# (the "License"); you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software distributed 
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
# CONDITIONS OF ANY KIND, either express or implied. See the License for the 
# specific language governing permissions and limitations under the License.
# __END_LICENSE__

from collections import OrderedDict

from django.conf import settings
from django.forms.fields import ChoiceField
from django.forms.models import ModelChoiceField

from geocamUtil.models import SiteFrame

class SiteframeChoiceField(ModelChoiceField):
    """Uses the name in siteframe to map to the dictionary identifier in settings
    """
    def __init__(self, choices=(), required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):
        if not initial:
            initial = SiteFrame.objects.get(pk=settings.XGDS_CURRENT_SITEFRAME_ID)
        SITE_FRAMES = SiteFrame.objects.all().order_by('name')
        super(SiteframeChoiceField, self).__init__(queryset=SITE_FRAMES, required=required, widget=widget, label=label,
                                                   initial=initial, help_text=help_text, *args, **kwargs)
       
    def label_from_instance(self, obj):
        return obj.name

# class SiteframeChoiceField(ChoiceField):
#     """Uses the name in siteframe to map to the dictionary identifier in settings
#     """
#     def __init__(self, choices=(), required=True, widget=None, label=None,
#                  initial=None, help_text=None, *args, **kwargs):
#         sfChoices = []
#         sfChoices.extend(choices)
#         od = OrderedDict(sorted(settings.XGDS_SITEFRAMES.items(), key=lambda t: t[1]['name']))
#         for key, value in od.iteritems():
#             sfChoices.append((key, value['name']))
#         super(SiteframeChoiceField, self).__init__(choices=tuple(sfChoices), required=required, widget=widget, label=label,
#                                                    initial=initial, help_text=help_text, *args, **kwargs)