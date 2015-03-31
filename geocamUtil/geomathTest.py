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

import geomath


class GeoMathTest(unittest.TestCase):
    def assertVectorAlmostEqual(self, v1, v2):
        for i, val1 in enumerate(v1):
            val2 = v2[i]
            self.assertAlmostEqual(val1, val2)

    def test1(self):
        originLonLatAlt = (-121, 37, 0)
        enu = (1000, 1000, 1000)
        lonLatAlt = geomath.transformEnuToLonLatAlt(originLonLatAlt, enu)
        correct = (-120.98876595195931, 37.00900886849891, 1000.1569072734565)
        self.assertVectorAlmostEqual(lonLatAlt, correct)

if __name__ == '__main__':
    unittest.main()
