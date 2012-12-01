# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

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
    add_introspection_rules([], ["^geocamUtil\.models\.ExtrasDotField"])
except ImportError:
    pass
