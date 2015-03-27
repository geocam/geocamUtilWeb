# __BEGIN_LICENSE__
#Copyright © 2015, United States Government, as represented by the 
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
# __END_LICENSE__

import logging

from geocamUtil.management import commandUtil


class Command(commandUtil.PathCommand):
    help = 'Execute management/appCommands/prep.py for each app in the site'

    def handleImportPaths(self, impPaths, options):
        for impPath in impPaths:
            prepImpPath = '%s.management.appCommands.prep' % impPath

            try:
                appPrepMod = __import__(prepImpPath, fromlist=['dummy'])
            except ImportError:
                appPrepMod = None

            if not appPrepMod:
                logging.debug('skipping %s, could not import %s (check for __init__.py files in directory hierarchy)',
                              impPath, prepImpPath)
                continue

            cmd = appPrepMod.Command()
            cmd.handle(**options)
