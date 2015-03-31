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

import re
from django.forms import fields
from django.core.exceptions import ValidationError


class UuidField(fields.CharField):
    """Accepts an input UUID in the format you would get
    from str(uuid.uuid4())."""
    def __init__(self, **kwargs):
        kwargs.setdefault('max_length', 128)
        super(UuidField, self).__init__(**kwargs)

    def clean(self, value):
        value = super(UuidField, self).clean(value)
        value = value.strip().lower()
        if value in fields.EMPTY_VALUES:
            return u''
        if re.search(r'^[0-9a-f\-]{36}$', value):
            return value
        else:
            raise ValidationError('Input string is not a valid UUID (should look like output of Python str(uuid.uuid4())).')
