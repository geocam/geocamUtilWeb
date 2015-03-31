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

from UuidField import UuidField
from ExtrasField import ExtrasField
from dateTimeUtc import DateTimeUtcField
from timestampDescriptor import TimestampDescriptor
from AbstractEnum import AbstractEnumModel
from jsonField import (JsonCharField,
                       JsonTextField)


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


class JsonExample(models.Model):
    """The sole purpose of this model is to test the JSON field types."""
    intChar = JsonCharField(max_length=80, valueType='array<int>')
    floatChar = JsonCharField(max_length=80, valueType='array<float>')
    intText = JsonTextField(valueType='array<int>')
    floatText = JsonTextField(valueType='array<float>')
