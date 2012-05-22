from datetime import datetime, timedelta

class TimestampDescriptor(object):
    """
    This descriptor class combines a second-resolution timestamp field with an 
    auxilliary float field that represents microseconds.
    """

    def __init__(self, seconds_field, microseconds_field):
        self.seconds_field = seconds_field
        self.microseconds_field = microseconds_field

    def __get__(self, instance, owner):
        timestamp = getattr(instance, self.seconds_field)
        assert isinstance(timestamp, datetime)
        return timestamp + timedelta(microseconds=getattr(instance, self.microseconds_field))

    def __set__(self, instance, value):
        assert isinstance( value, datetime )
        microseconds = value.microsecond
        setattr(instance, self.seconds_field, value - timedelta(microseconds=microseconds) )
        setattr(instance, self.microseconds_field, microseconds)
