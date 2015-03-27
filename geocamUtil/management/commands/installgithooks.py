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

import os
import sys
import glob
from optparse import make_option

from django.core.management.base import BaseCommand

from geocamUtil.management.commandUtil import getSiteDir, dosys


class Command(BaseCommand):
    help = 'Install git hooks from geocamUtil/management/githooks'

    option_list = BaseCommand.option_list + (
        make_option('-f', '--force',
                    action='store_true',
                    default=False,
                    help='Overwrite any existing hooks'),
    )

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))
        force = options.get('force', False)

        siteDir = getSiteDir()
        srcDir = os.path.join(siteDir, 'apps', 'geocamUtil', 'management', 'githooks')
        hookFiles = os.listdir(srcDir)

        dotGitDirs = ['%s.git' % siteDir] + glob.glob('%s.git/modules/submodules/*' % siteDir)

        for dotGitDir in dotGitDirs:
            tgtDir = os.path.join(dotGitDir, 'hooks')
            if not os.path.exists(tgtDir):
                dosys('mkdir -p %s' % tgtDir, verbosity)
            srcRelTgt = os.path.relpath(os.path.realpath(srcDir),
                                        os.path.realpath(tgtDir))
            for f in hookFiles:
                tgtPath = os.path.join(tgtDir, f)
                if os.path.exists(tgtPath):
                    if force:
                        dosys('rm -f %s' % tgtPath, verbosity)
                    else:
                        continue
                srcPath = os.path.join(srcRelTgt, f)
                dosys('ln -s %s %s' % (srcPath, tgtPath), verbosity)
