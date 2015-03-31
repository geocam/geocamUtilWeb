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
