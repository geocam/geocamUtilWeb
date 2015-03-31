# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import shutil
import unittest
import tempfile
import logging

from geocamUtil.store import FileStore, LruCacheStore


class StoreTest(unittest.TestCase):
    def storeTest(self, storeFactory):
        tempDir = tempfile.mkdtemp('-storeTestDir')

        store1 = storeFactory(tempDir)
        for i in xrange(20):
            store1[str(i)] = i
        store1.sync()

        store2 = storeFactory(tempDir)
        for i in xrange(20):
            self.assertEqual(store2[str(i)], i)

        shutil.rmtree(tempDir)

    def test_FileStore(self):
        self.storeTest(FileStore)

    def test_LruCacheStore(self):
        self.storeTest(lambda path: LruCacheStore(FileStore(path), 5))

#    def test_LruEvict(self):
#        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
