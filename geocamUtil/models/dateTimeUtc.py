# __NO_RELICENSE__

"""
The DateTimeUtcField is a convenience field to help with transitioning
to Django 1.4 time zone handling.

If we are in Django < 1.4 and settings.USE_TZ = True, DateTimeUtcField
provides an interface to application code which looks like Django 1.4's
version of DateTimeField. This means it expects datetime values to have
their tzinfo set ("non-naive"), and it converts them to the UTC time
zone before saving.

In all other cases, DateTimeUtcField is basically just an alias for
DateTimeField.

To use it, replace:

  class MyModel(models.Model):
      timestamp = models.DateTimeField()

with this:

  from geocamUtil.models import DateTimeUtcField

  class MyModel(models.Model):
      timestamp = DateTimeUtcField()

Note: Most of the code in this file is copied from the Django 1.4.0
distribution.
"""

import datetime
import warnings

import django
from django.db import models
from django.db.models import DateTimeField
from django.conf import settings
from django.utils.encoding import smart_str
from django.core import exceptions

from geocamUtil import timezone
from geocamUtil.dateparse import parse_date, parse_datetime


def backportTimeZone():
    return (getattr(settings, 'USE_TZ', False)
            and django.VERSION < (1, 4))


class DateTimeUtcField(models.DateTimeField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if not backportTimeZone():
            return super(DateTimeUtcField, self).to_python(value)

        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            if timezone.is_naive(value):
                value = timezone.make_aware(value, timezone.utc)
            return value
        if isinstance(value, datetime.date):
            value = datetime.datetime(value.year, value.month, value.day)
            if settings.USE_TZ:
                # For backwards compatibility, interpret naive datetimes in
                # local time. This won't work during DST change, but we can't
                # do much about it, so we let the exceptions percolate up the
                # call stack.
                warnings.warn(u"DateTimeField received a naive datetime (%s)"
                              u" while time zone support is active."
                              u" Converting from default time zone to UTC." % value,
                              RuntimeWarning)
                default_timezone = timezone.get_default_timezone()
                value = timezone.make_aware(value, default_timezone)
            return value

        value = smart_str(value)

        try:
            parsed = parse_datetime(value)
            if parsed is not None:
                return parsed
        except ValueError:
            msg = self.error_messages['invalid_datetime'] % value
            raise exceptions.ValidationError(msg)

        try:
            parsed = parse_date(value)
            if parsed is not None:
                return datetime.datetime(parsed.year, parsed.month, parsed.day)
        except ValueError:
            msg = self.error_messages['invalid_date'] % value
            raise exceptions.ValidationError(msg)

        msg = self.error_messages['invalid'] % value
        raise exceptions.ValidationError(msg)

    # pylint: disable=E1003
    def pre_save(self, model_instance, add):
        if not backportTimeZone():
            return super(DateTimeUtcField, self).pre_save(model_instance, add)

        if self.auto_now or (self.auto_now_add and add):
            value = timezone.now()
            setattr(model_instance, self.attname, value)
            return value
        else:
            # Note this is purposefully calling the pre_save() method
            # from the super-super-class, not the super-class.
            return super(DateTimeField, self).pre_save(model_instance, add)

    def get_prep_value(self, value):
        if not backportTimeZone():
            return super(DateTimeUtcField, self).get_prep_value(value)

        value = self.to_python(value)
        if value is not None and settings.USE_TZ and timezone.is_naive(value):
            # For backwards compatibility, interpret naive datetimes in local
            # time. This won't work during DST change, but we can't do much
            # about it, so we let the exceptions percolate up the call stack.
            warnings.warn(u"DateTimeField received a naive datetime (%s)"
                          u" while time zone support is active."
                          u" Converting from default time zone to UTC." % value,
                          RuntimeWarning)
            default_timezone = timezone.get_default_timezone()
            value = timezone.make_aware(value, default_timezone)

        # And, after all that mimicking of the Django 1.4 logic, in the
        # end we need to strip the tzinfo because the pre-1.4 ORM can't
        # handle it.
        value = timezone.make_naive(value, timezone.utc)

        return value


try:
    from south.modelsinspector import add_introspection_rules
    # tell south it can freeze this field without any special nonsense
    add_introspection_rules([], ["^geocamUtil\.models\.DateTimeUtcField"])
except ImportError:
    pass
