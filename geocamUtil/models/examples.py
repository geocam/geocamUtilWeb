# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.db import models

from UuidField import UuidField
from dateTimeUtc import DateTimeUtcField
from timestampDescriptor import TimestampDescriptor
from AbstractEnum import AbstractEnumModel
from jsonField import (JsonCharField,
                       JsonTextField)
from geocamUtil.models.ExtrasDotField import ExtrasDotField


class UuidExample(models.Model):
    """The sole purpose of this model is to test the UuidField class."""
    uuid = UuidField()

    class Meta:
        app_label="geocamUtil"

class ExtrasExample(models.Model):
    """The sole purpose of this model is to test the ExtrasDotField class."""
    extras = ExtrasDotField()

    class Meta:
        app_label="geocamUtil"

class DateTimeUtcExample(models.Model):
    """The sole purpose of this model is to test the DateTimeUtcField class."""
    timestamp = DateTimeUtcField()

    class Meta:
        app_label="geocamUtil"

class TimestampDescriptorExample(models.Model):
    """
    The sole purpose of this model is to test the TimestampDescriptor class.
    """
    timestampSeconds = models.DateTimeField(null=True, blank=True)
    timestampMicroseconds = models.PositiveIntegerField(default=0)
    timestamp = TimestampDescriptor('timestampSeconds', 'timestampMicroseconds')

    class Meta:
        app_label="geocamUtil"

class JsonExample(models.Model):
    """The sole purpose of this model is to test the JSON field types."""
    intChar = JsonCharField(max_length=80, valueType='array<int>')
    floatChar = JsonCharField(max_length=80, valueType='array<float>')
    intText = JsonTextField(valueType='array<int>')
    floatText = JsonTextField(valueType='array<float>')

    class Meta:
        app_label="geocamUtil"
