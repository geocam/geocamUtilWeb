# __BEGIN_LICENSE__
#Copyright © 2015, United States Government, as represented by the 
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
# __END_LICENSE__

from datetime import datetime


class TimestampDescriptor(object):
    """
    Descriptor that supports storage of high-resolution timestamps in a
    Django model.

    Many SQL databases don't have native support for high-resolution
    timestamps, and the Django ORM may not support high-resolution time
    even if the underlying database does. To fill this gap, we designed
    a descriptor that helps you split up a high-resolution timestamp
    into a database-native DateTimeField and a PositiveIntegerField that
    represents the fractional seconds part of the time as an integer
    number of microseconds.

    This allows you to work with the second-resolution part of the time
    in database-specific admin tools and the Django admin interface,
    while keeping the fractional part around in case, for example, your
    rows represent telemetry messages coming in at a rate faster than one
    per second and you need to keep track of their exact ordering.

    Example usage:

    from geocamUtil.models.timestampDescriptor import TimestampDescriptor

    class SomeModel(models.Model):
        timestampSeconds = models.DateTimeField()
        timestampMicroseconds = models.PositiveIntegerField(default=0)
        timestamp = TimestampDescriptor('timestampSeconds', 'timestampMicroseconds')

    >> s = SomeModel()
    >> now = datetime.datetime.now()
    >> now
    datetime.datetime(2012, 5, 22, 7, 37, 16, 689212)
    >> s.timestamp = now
    >> s.timestampSeconds
    datetime.datetime(2012, 5, 22, 7, 37, 16)
    >> s.timestampMicroseconds
    689212

    """

    def __init__(self, secondsField, microsecondsField):
        self.secondsField = secondsField
        self.microsecondsField = microsecondsField

    def __get__(self, instance, owner):
        timestampSeconds = getattr(instance, self.secondsField)
        timestampMicroseconds = getattr(instance, self.microsecondsField)
        if timestampSeconds is None:
            return None
        else:
            assert isinstance(timestampSeconds, datetime)
            return timestampSeconds.replace(microsecond=timestampMicroseconds)

    def __set__(self, instance, timestamp):
        if timestamp is None:
            timestampSeconds = None
            timestampMicroseconds = 0
        else:
            assert isinstance(timestamp, datetime)
            timestampSeconds = timestamp.replace(microsecond=0)
            timestampMicroseconds = timestamp.microsecond
        setattr(instance, self.secondsField, timestampSeconds)
        setattr(instance, self.microsecondsField, timestampMicroseconds)
