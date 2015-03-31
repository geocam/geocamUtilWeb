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
        try:
            svg.buildIcon(builder, srcImage, outputDir=self.outDir)
        except svg.NoSvgBackendError:
            logging.warning('no svg rendering backend found')
            logging.warning('in order to run svg rendering tests, try installing ImageMagick or rsvg')
            logging.warning('note: this may be ok; svg rendering may not be needed for your site')
            return
        self.assertExists('%sexample.png' % self.outDir)
        self.assertExists('%sexamplePoint.png' % self.outDir)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
