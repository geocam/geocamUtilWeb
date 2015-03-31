# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the
#Administrator of the National Aeronautics and Space Administration.
#All rights reserved.
# __END_LICENSE__
# __BEGIN_APACHE_LICENSE__
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
# __END_APACHE_LICENSE__

try:
    import uuid
except ImportError:
    uuid = None

from django.db import models

if uuid:
    def makeUuid():
        return str(uuid.uuid4())
else:
    import random

    def makeUuid():
        return '%04x-%02x-%02x-%02x-%06x' % (random.getrandbits(32), random.getrandbits(8),
                                             random.getrandbits(8), random.getrandbits(8),
                                             random.getrandbits(48))


class UuidField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 48)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('db_index', True)
        super(UuidField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.attname):
            value = makeUuid()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UuidField, self).pre_save(model_instance, add)

try:
    from south.modelsinspector import add_introspection_rules
    # tell south it can freeze this field without any special nonsense
    add_introspection_rules([], [r'^geocamUtil\.models\.UuidField'])
except ImportError:
    pass
