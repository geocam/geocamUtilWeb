# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

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
