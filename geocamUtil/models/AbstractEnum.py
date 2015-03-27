# __BEGIN_LICENSE__
#Copyright © 2015, United States Government, as represented by the 
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

from django.db import models

# pylint: disable=C1001


class AbstractEnumModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['display_name']
    value = models.CharField(max_length=256)
    display_name = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return self.display_name or self.value
