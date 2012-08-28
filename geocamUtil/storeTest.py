# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import shutil
import unittest
import tempfile

from geocamUtil.store import FileStore, LruCacheStore


class StoreTest(unittest.TestCase):
    def storeTest(self, storeFactory):
        tempDir = tempfile.mkdtemp('-storeTestDir')

        store1 = storeFactory(tempDir)
        store1['a'] = 1
        store1['b'] = 2
        store1.sync()

        store2 = storeFactory(tempDir)
        self.assertEqual(store2['a'], 1)
        self.assertEqual(store2['b'], 2)

        shutil.rmtree(tempDir)

    def test_FileStore(self):
        self.storeTest(FileStore)

    def test_LruCacheStore(self):
        self.storeTest(lambda path: LruCacheStore(FileStore(path), 100))
