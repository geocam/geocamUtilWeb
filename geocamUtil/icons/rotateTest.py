# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

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
