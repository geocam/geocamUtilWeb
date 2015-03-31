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

from django.db import models
from django.core.exceptions import ValidationError

from geocamUtil import anyjson as json
from geocamUtil.dotDict import DotDict, convertToDotDictRecurse


class ExtrasDotField(models.TextField):
    """
    A Django model field for storing extra schema-free data.  You can
    get and set arbitrary properties on the extra field, which can be
    comprised of strings, numbers, dictionaries, arrays, booleans, and
    None.  These properties are stored in the database as a JSON-encoded
    set of key-value pairs.
    """

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargsin):
        kwargs = dict(blank=True)
        kwargs.update(**kwargsin)
        super(ExtrasDotField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value == '':
            return DotDict()
        elif type(value) == DotDict:
            return value
        else:
            extras = DotDict()
            try:
                values = convertToDotDictRecurse(json.loads(value))
                assert isinstance(values, DotDict), 'expected a DotDict object, found a %s' % type(values).__name__
                for key in values.iterkeys():
                    assert type(key) in (unicode, str), 'expected unicode or str keys, found a %s' % type(key).__name__
                extras = values
            except (ValueError, AssertionError), e:
                raise ValidationError('Invalid JSON data in ExtrasDotField: %s' % e)
            return extras

    def get_db_prep_value(self, value, connection=None, prepared=False):
        return str(value)

try:
    from south.modelsinspector import add_introspection_rules
    # tell south it can freeze this field without any special nonsense
    add_introspection_rules([], [r'^geocamUtil\.models\.ExtrasDotField'])
except ImportError:
    pass
