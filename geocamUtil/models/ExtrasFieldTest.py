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

from django.test import TestCase

from geocamUtil.models import ExtrasExample


class ExtrasFieldTest(TestCase):
    def setUp(self):
        self.obj = ExtrasExample()
        self.obj.extras.a = 1
        self.obj.extras.b = 'foo'
        self.obj.save()

    def test_recoverContents(self):
        obj2 = ExtrasExample.objects.get(id=self.obj.id)
        self.assertEqual(obj2.extras.a, 1)
        self.assertEqual(obj2.extras.b, 'foo')
