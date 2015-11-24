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
        query = "select MAX(CAST(SUBSTRING_INDEX(id, '_', -1) AS UNSIGNED)) " + \
                "from %s where id like '%s_%%'" % (cls._meta.db_table, HOSTNAME)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if result[0] is not None:
            index = int(result[0]) + 1
        else:
            index = 1
        cursor.close()
        return index
    
    @classmethod
    def getKey(cls):
        keyName = "using_" + str(cls.__name__)
        if not cache.add(keyName, True, 10):  # Should never have key for > 10 sec.
            count = 0
            # now we have to wait
            keyLock = False
            while not keyLock and count<10:
                time.sleep(0.001)
                keyLock = cache.add(keyName, True, 10)
                count += 1
            if not keyLock:
                raise Exception("Could not get lock on PK to insert into " + cls.__name__)
        return keyName
        
    @classmethod
    def getNextId(cls):
        # get the key to use for this table and grab lock on it
        keyName = cls.getKey()
            
        try:
            index = int(cache.incr(cls.__name__))  # get PK index from cache and bump up by 1
        except:
            # Key index not cached, initialize from DB
            index = cls.getUniqueIndex()
            cache.set(cls.__name__,index)

        cache.delete(keyName) # Release lock on key
        return index

    def fillId(self):
        next_id = self.getNextId()
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
