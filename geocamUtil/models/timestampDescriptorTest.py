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
