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

import re

from django.test import TestCase

from geocamUtil.models import UuidExample


class UuidFieldTest(TestCase):
    def setUp(self):
        self.u = UuidExample()
        self.u.save()

    def test_format(self):
        self.assert_(re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', self.u.uuid))

    def test_getById(self):
        u2 = UuidExample.objects.get(id=self.u.id)
        self.assertEqual(self.u.uuid, u2.uuid)

    def test_getByUuid(self):
        u2 = UuidExample.objects.get(uuid=self.u.uuid)
        self.assertEqual(self.u.id, u2.id)
