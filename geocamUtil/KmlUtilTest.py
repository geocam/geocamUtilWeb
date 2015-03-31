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

import KmlUtil


class KmlMarkersTest(unittest.TestCase):
    def assertStripEqual(self, a, b):
        self.assertEqual(a.strip(), b.strip())

    def test_format1(self):
        points = [[-122, 37],
                  [-123, 38]]
        self.assertStripEqual(KmlUtil.markers(points),
                              """
<Placemark>
  <name>0</name>
  <Point>
    <coordinates>-122,37</coordinates>
  </Point>
</Placemark>
<Placemark>
  <name>1</name>
  <Point>
    <coordinates>-123,38</coordinates>
  </Point>
</Placemark>
""")

    def test_format2(self):
        points = {'foo': [-122, 37],
                  'bar': [-123, 38]}
        self.assertStripEqual(KmlUtil.markers(points),
                              """
<Placemark>
  <name>foo</name>
  <Point>
    <coordinates>-122,37</coordinates>
  </Point>
</Placemark>
<Placemark>
  <name>bar</name>
  <Point>
    <coordinates>-123,38</coordinates>
  </Point>
</Placemark>
""")

    def test_format3(self):
        points = {'foo': {'lat': 37, 'lon': -122},
                  'bar': {'lat': 38, 'lon': -123}}
        self.assertStripEqual(KmlUtil.markers(points,
                                              latitude='lat',
                                              longitude='lon'),
                              """
<Placemark>
  <name>foo</name>
  <Point>
    <coordinates>-122,37</coordinates>
  </Point>
</Placemark>
<Placemark>
  <name>bar</name>
  <Point>
    <coordinates>-123,38</coordinates>
  </Point>
</Placemark>
""")

    def test_format4(self):
        points = [{'title': 'foo', 'x': -122, 'y': 37},
                  {'title': 'bar', 'x': -123, 'y': 38}]
        self.assertStripEqual(KmlUtil.markers(points,
                                              name='title',
                                              longitude='x',
                                              latitude='y'),
                              """
<Placemark>
  <name>foo</name>
  <Point>
    <coordinates>-122,37</coordinates>
  </Point>
</Placemark>
<Placemark>
  <name>bar</name>
  <Point>
    <coordinates>-123,38</coordinates>
  </Point>
</Placemark>
""")


if __name__ == '__main__':
    unittest.main()
