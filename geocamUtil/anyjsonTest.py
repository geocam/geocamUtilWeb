# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
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
