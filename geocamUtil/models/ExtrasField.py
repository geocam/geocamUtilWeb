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
from geocamUtil.models.ExtrasDotField import convertToDotDictRecurse


class DotDict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Extras(object):
    # At the moment this object exists pretty much solely to let you
    # get and set elements in its __dict__ dictionary via dotted
    # notation.  Someday it could do more.
    def __repr__(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=True)

    # This is here mostly so you can use the "in" keyword.
    def __iter__(self):
        return self.__dict__.__iter__()

    def toDotDict(self):
        """
        Convenience function to use if you want to use dot notation recursively
        everywhere within the parsed JSON.
        """
        return DotDict(dict([(k, convertToDotDictRecurse(v))
                             for k, v in self.__dict__.iteritems()]))


class ExtrasField(models.TextField):
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
        super(ExtrasField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value == '':
            return Extras()
        elif type(value) == Extras:
            return value
        else:
            extras = Extras()
            try:
                values = json.loads(value)
                assert type(values) == dict, 'expected a dictionary object, found a %s' % type(values).__name__
                for key in values.keys():
                    assert type(key) in (unicode, str), 'expected unicode keys, found a %s' % type(key).__name__
                extras.__dict__ = values  # pylint: disable=W0201
            except (ValueError, AssertionError), e:
                raise ValidationError('Invalid JSON data in ExtrasField: %s' % e)
            return extras

    def get_db_prep_value(self, value, connection=None, prepared=False):
        return json.dumps(value.__dict__)

try:
    from south.modelsinspector import add_introspection_rules
    # tell south it can freeze this field without any special nonsense
    add_introspection_rules([], [r'^geocamUtil\.models\.ExtrasField'])
except ImportError:
    pass
