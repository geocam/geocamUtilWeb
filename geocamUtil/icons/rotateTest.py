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

import logging
import unittest
import tempfile
import shutil
import os

from geocamUtil.icons import rotate
from geocamUtil.Builder import Builder


class IconsTest(unittest.TestCase):
    def setUp(self):
        self.outDir = tempfile.mkdtemp() + os.path.sep

    def tearDown(self):
        shutil.rmtree(self.outDir)

    def assertExists(self, path):
        logging.debug('assertExists %s', path)
        self.assert_(os.path.exists(path))


class IconsRotateTest(IconsTest):
    def test_buildAllDirections(self):
        thisDir = os.path.dirname(os.path.abspath(__file__))
        srcImage = '%s/media_src/icons/example.png' % os.path.dirname(thisDir)

        builder = Builder()
        logging.debug('buildAllDirections srcImage=%s outDir=%s', srcImage, self.outDir)
        rotate.buildAllDirections(builder, srcImage, self.outDir)
        self.assertExists('%sexample000.png' % self.outDir)
        self.assertExists('%sexample180.png' % self.outDir)
        self.assertExists('%sexample350.png' % self.outDir)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
