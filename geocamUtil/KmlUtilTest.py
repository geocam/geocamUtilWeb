# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

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
