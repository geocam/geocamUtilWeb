# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

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
