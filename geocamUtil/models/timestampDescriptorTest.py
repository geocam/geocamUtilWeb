# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import datetime

from django.test import TestCase

from geocamUtil.models import TimestampDescriptorExample

# pylint: disable=E1101


class TimestampDescriptorTest(TestCase):
    def setUp(self):
        pass

    def test_standard(self):
        ts = datetime.datetime(2012, 5, 22, 7, 37, 16, 689212)
        obj = TimestampDescriptorExample()
        obj.timestamp = ts
        obj.save()

        obj2 = TimestampDescriptorExample.objects.get(id=obj.id)

        self.assertEqual(obj.timestampSeconds, obj2.timestampSeconds)
        self.assertEqual(obj.timestampSeconds.second, 16)
        self.assertEqual(obj2.timestampSeconds.second, 16)
        self.assertEqual(obj.timestampMicroseconds, 689212)
        self.assertEqual(obj2.timestampMicroseconds, 689212)

    def test_none(self):
        obj = TimestampDescriptorExample()
        obj.timestamp = None
        obj.save()

        obj2 = TimestampDescriptorExample.objects.get(id=obj.id)

        self.assertEqual(obj.timestampSeconds, None)
        self.assertEqual(obj2.timestampSeconds, None)
        self.assertEqual(obj.timestampMicroseconds, 0)
        self.assertEqual(obj2.timestampMicroseconds, 0)
