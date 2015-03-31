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

import unittest

from MultiSettings import MultiSettings


class Container(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class MultiSettingsTest(unittest.TestCase):
    def setUp(self):
        mod1 = Container(a=1, b=2)
        mod2 = Container(b=99, c=3)
        self.settings = MultiSettings(mod1, mod2)

    def test_first(self):
        self.assertEqual(self.settings.a, 1)

    def test_order(self):
        self.assertEqual(self.settings.b, 2)

    def test_second(self):
        self.assertEqual(self.settings.c, 3)

    def test_missing(self):
        self.assertRaises(AttributeError, lambda: self.settings.d)

if __name__ == '__main__':
    unittest.main()
