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
import sys
import django

from optparse import make_option

from django.core.management.base import BaseCommand

from geocamUtil.management.commandUtil import getSiteDir, dosys
from geocamUtil import settings

"""
It turns out you can compress directly from compass by configuring the config.rb to compress.  Who knew? 
Anyhow no longer any need to call yuglify.
"""
class Command(BaseCommand):
    help = 'Use compass to compile css from sass in various directories.  Ruby, compass, and your gems must be installed'

    option_list = BaseCommand.option_list + (
        make_option('-c', '--compress',
                    action='store_true',
                    default=False,
                    help='Use Yuglify to compress the new css'),
    )

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))
        compress = options.get('compress', False)

        siteDir = getSiteDir()
        staticRoot = getattr(settings, 'STATIC_ROOT', '%sbuild/static' % siteDir)

        for cssDir in getattr(settings, 'GEOCAM_UTIL_PREPCSS_DIRS'):
            fullDir = os.path.join(staticRoot, cssDir)
            ret = os.chdir(fullDir)
            if ret != 0:
                if verbosity > 1:
                    print >> sys.stderr, ret
            if verbosity > 1:
                print 'about to compass %s' % fullDir
            dosys('compass clean ', verbosity)
            dosys('compass compile ', verbosity)
            if verbosity > 1:
                print 'done with compass'

        if compress:
            for compressFile in getattr(settings, 'GEOCAM_UTIL_COMPRESSCSS_FILES'):
                fullFile = os.path.join(staticRoot, compressFile)
                if verbosity > 1:
                    print 'about to compress %s' % fullFile
                dosys('yuglify %s' % fullFile, verbosity)
                if verbosity > 1:
                    print 'done compressing %s' % fullFile

