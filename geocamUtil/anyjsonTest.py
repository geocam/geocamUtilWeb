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

import unittest

import anyjson

JSON_STRING = '{"a": 1, "b": "foo"}'
JSON_OBJECT = dict(a=1, b='foo')


class AnyJsonTest(unittest.TestCase):
    def test_dumps(self):
        self.assertEqual(JSON_STRING, anyjson.dumps(JSON_OBJECT))

    def test_loads(self):
        self.assertEqual(JSON_OBJECT, anyjson.loads(JSON_STRING))

if __name__ == '__main__':
    unittest.main()
