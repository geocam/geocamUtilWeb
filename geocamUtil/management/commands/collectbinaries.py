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

import os
import logging

from geocamUtil.management import commandUtil
from geocamUtil.Installer import Installer


class Command(commandUtil.PathCommand):
    help = 'Collect binaries from all apps into build/bin'

    def handleImportPaths(self, impPaths, options):
        for impPath in impPaths:
            logging.debug('collectbinaries app %s', impPath)
            appMod = __import__(impPath, fromlist=['dummy'])
            appPath = os.path.dirname(appMod.__file__)
            binPath = '%s/bin' % appPath
            logging.debug('collectbinaries app %s: checking for binaries in %s', impPath, binPath)
            if os.path.exists(binPath):
                siteDir = commandUtil.getSiteDir()
                inst = Installer()
                inst.installRecurseGlob('%s/*' % binPath, '%sbuild/bin' % siteDir)
