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

import time

from django.core.cache import cache
from django.db import models
from django.db import connection

from geocamUtil.defaultSettings import HOSTNAME


class ServerIdModel(models.Model):
    ''' This abstract class generates unique character ids of the format servername_index, ie myserver_1, myserver_2.
    If you are synchronizing between multiple servers, it will find the largest index and add one.
    It makes use of memcached, so you must have:
    (in python)
    pylibmc
    (in ubuntu)
    memcached
    libmemcached-dev
    
    This uses memcached to store the largest index and to keep a semaphore for usage of the memcache.  It tries only 10 times for the key.
    '''
    
    # custom id field for uniqueness
    id = models.CharField(max_length=128,
                          unique=True, blank=False,
                          editable=False, primary_key=True)
    
    @classmethod
    def getUniqueIndex(cls):
        query = "select MAX(CAST(SUBSTRING_INDEX(id, '_', -1) AS UNSIGNED))  from " + cls._meta.db_table
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        try:
            index = int(result[0]) + 1
        except:
            index = 1
        finally:
            cursor.close()
        return index
    
    @classmethod
    def getKey(cls):
        keyName = "using_" + str(cls.__name__)
        key = cache.get(keyName)
        if not key:
            cache.set(keyName, True)
        else:
            count = 0
            # now we have to wait
            while key and count<10:
                time.sleep(0.001)
                key = cache.get(keyName)
                count = count + 1
            if not key:
                cache.set("using " + cls.__name__, True)
            else:
                raise Exception("Could not get key to insert into " + cls.__name__)
        return keyName
        
    @classmethod
    def getLastId(cls):
        # get the key to use this 
        keyName = cls.getKey()
            
        try:
            index = cache.get(cls.__name__)
            index = index + 1
        except:
            # Initializing
            index = cls.getUniqueIndex()
        cache.set(cls.__name__,index)
        cache.set(keyName, None)
            
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