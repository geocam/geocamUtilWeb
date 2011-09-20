# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import logging
import unittest
import os

from geocamUtil.icons import svg
from geocamUtil.Builder import Builder
from geocamUtil.icons import rotateTest


class IconsSvgTest(rotateTest.IconsTest):
    def test_buildIcon(self):
        thisDir = os.path.dirname(os.path.abspath(__file__))
        srcImage = '%s/media_src/icons/example.svg' % os.path.dirname(thisDir)

        builder = Builder()
        logging.debug('buildIcon srcImage=%s outDir=%s', srcImage, self.outDir)
        svg.buildIcon(builder, srcImage, outputDir=self.outDir)
        self.assertExists('%sexample.png' % self.outDir)
        self.assertExists('%sexamplePoint.png' % self.outDir)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
