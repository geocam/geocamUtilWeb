# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.db import models

from UuidField import UuidField
from ExtrasField import ExtrasField
from dateTimeUtc import DateTimeUtcField
from timestampDescriptor import TimestampDescriptor


class UuidExample(models.Model):
    """The sole purpose of this model is to test the UuidField class."""
    uuid = UuidField()


class ExtrasExample(models.Model):
    """The sole purpose of this model is to test the ExtrasField class."""
    extras = ExtrasField()


class DateTimeUtcExample(models.Model):
    """The sole purpose of this model is to test the DateTimeUtcField class."""
    timestamp = DateTimeUtcField()


class TimestampDescriptorExample(models.Model):
    """
    The sole purpose of this model is to test the TimestampDescriptor class.
    """
    timestampSeconds = models.DateTimeField(null=True, blank=True)
    timestampMicroseconds = models.PositiveIntegerField(default=0)
    timestamp = TimestampDescriptor('timestampSeconds', 'timestampMicroseconds')
