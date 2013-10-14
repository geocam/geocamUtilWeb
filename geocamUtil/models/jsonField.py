# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.db import models

from geocamUtil import anyjson as json


class JsonMixin(object):
    def to_python(self, value):
        if value in ('', None):
            return None
        elif isinstance(value, (str, unicode)):
            return json.loads(value)
        else:
            return value

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if value is None:
            return value
        return json.dumps(value, separators=',:')


class JsonCharField(JsonMixin, models.CharField):
    """
    Encodes a Python value as JSON in a Django CharField.

    The required 'max_length' parameter specifies the maximum size of
    JSON representation the field can hold.  If you can't guarantee a
    length bound, use JsonTextField instead.

    The optional 'valueType' parameter annotates what type the stored
    values are expected to have but is otherwise ignored.

    You can store any JSON-encodable object (primitive type, list,
    tuple, dict, etc.) *except* a string or unicode object. Due to
    quirks of Django, trying to store a string or unicode object is
    likely to cause confusion during packing/unpacking.
    """
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargsin):
        kwargs = {
            'blank': True
        }
        kwargs.update(**kwargsin)
        self.valueType = kwargs.pop('valueType', None)
        super(JsonCharField, self).__init__(*args, **kwargs)


class JsonTextField(JsonMixin, models.TextField):
    """
    Encodes a Python value as JSON in a Django TextField.

    JsonTextField can hold JSON representations of arbitrary length,
    possibly at the cost of reduced performance relative to
    JsonCharField when storing small arrays.

    The optional 'valueType' parameter annotates what type the stored
    values are expected to have but is otherwise ignored.

    You can store any JSON-encodable object (primitive type, list,
    tuple, dict, etc.) *except* a string or unicode object. Due to
    quirks of Django, trying to store a string or unicode object is
    likely to cause confusion during packing/unpacking.
    """
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargsin):
        kwargs = {
            'blank': True
        }
        kwargs.update(**kwargsin)
        self.valueType = kwargs.pop('valueType', None)
        super(JsonTextField, self).__init__(*args, **kwargs)


try:
    from south.modelsinspector import add_introspection_rules
    # tell south it can freeze this field without any special nonsense
    add_introspection_rules([], [r'^geocamUtil\.models\.JsonCharField'])
    add_introspection_rules([], [r'^geocamUtil\.models\.JsonTextField'])
except ImportError:
    pass
