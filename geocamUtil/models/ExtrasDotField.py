# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__
import json
from django.db import models
from django.core.exceptions import ValidationError

from geocamUtil.dotDict import DotDict, convertToDotDictRecurse


class ExtrasDotField(models.TextField):
    """
    A Django model field for storing extra schema-free data.  You can
    get and set arbitrary properties on the extra field, which can be
    comprised of strings, numbers, dictionaries, arrays, booleans, and
    None.  These properties are stored in the database as a JSON-encoded
    set of key-value pairs.
    """

    def __init__(self, *args, **kwargsin):
        kwargs = dict(blank=True)
        if "default" not in kwargsin:
            kwargs["default"] = DotDict()
        kwargs.update(**kwargsin)
        super(ExtrasDotField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def to_python(self, value):
        ''' Takes json string from database and builds a DotDict structure
        '''
        if value == '':
            return DotDict()
        elif type(value) == DotDict:
            return value
        else:
            theDotDict = DotDict()
            try:
                jsonStruct = json.loads(value)
                theDotDict = convertToDotDictRecurse(jsonStruct)
                assert isinstance(theDotDict, DotDict), 'expected a DotDict object, found a %s' % type(theDotDict).__name__
                for key in theDotDict.iterkeys():
                    assert type(key) in (unicode, str), 'expected unicode or str keys, found a %s' % type(key).__name__
            except (ValueError, AssertionError), e:
                raise ValidationError('Invalid JSON data in ExtrasDotField: %s' % e)
            return theDotDict

    def get_db_prep_value(self, value, connection=None, prepared=False):
        return str(value)
