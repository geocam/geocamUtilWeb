# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.db import models
from django.core.exceptions import ValidationError

from geocamUtil import anyjson as json


def convertToDotDictRecurse(struct):
    if isinstance(struct, dict):
        for k, v in struct.iteritems():
            struct[k] = convertToDotDictRecurse(v)
        return DotDict(struct)
    elif isinstance(struct, list):
        return [convertToDotDictRecurse(elt) for elt in struct]
    else:
        return struct


class DotDict(dict):
    # At the moment this object exists pretty much solely to let you
    # get and set elements in its __dict__ dictionary via dotted
    # notation.  Someday it could do more.

    # these are fields that must not be defined to avoid causing problems
    # with Django
    _badFields = ('prepare_database_save',)

    def __repr__(self):
        return json.dumps(self, sort_keys=True, indent=4)

    def __getattr__(self, attr):
        if attr in self._badFields:
            raise KeyError(attr)
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


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
