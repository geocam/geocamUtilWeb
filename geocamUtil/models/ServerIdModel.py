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

from django.db import models
from geocamUtil.defaultSettings import HOSTNAME

index_map = {}

class ServerIdModel(models.Model):
    # custom id field for uniqueness
    id = models.CharField(max_length=128,
                          unique=True, blank=False,
                          editable=False, primary_key=True)
    
    @classmethod
    def getSafeIndex(cls, index):
        pk_test = HOSTNAME + "_" + str(index)
        try:
            cls.objects.get(pk=pk_test)
            return cls.getSafeIndex(index + 1)
        except:
            return index

    @classmethod
    def getLastId(cls, index=None):
        if not index:
            try:
                index = index_map[cls.__name__]
                index_map[cls.__name__] = index + 1
            except:
                # Initializing
                if cls.objects.count():
                    index = cls.objects.count() + 1
                else:
                    index = 0
                index = cls.getSafeIndex(index)
                index_map[cls.__name__] = index
            
            return index

    def fillId(self):
        next_id = self.getLastId()
        self.pk = HOSTNAME + "_" + str(next_id)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.fillId()
        self.preSave()
        super(ServerIdModel, self).save(*args, **kwargs)

    def preSave(self):
        """
        This is so derived classes can do stuff just before saving
        """
        return
    
    class Meta:
        abstract = True