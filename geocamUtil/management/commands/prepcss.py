# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import os
import sys
import django

from optparse import make_option

from django.core.management.base import BaseCommand

from geocamUtil.management.commandUtil import getSiteDir, dosys
from django.conf import settings

"""
It turns out you can compress directly from compass by configuring the config.rb to compress.  Who knew? 
Anyhow no longer any need to call yuglify.
"""
class Command(BaseCommand):
    help = 'Use compass to compile css from sass in various directories.  Ruby, compass, and your gems must be installed'

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument('--compress',
                            action='store_true',
                            default=False,
                            help='Use Yuglify to compress the new css')
    
    

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))
        compress = options.get('compress', False)

        siteDir = getSiteDir()
        staticRoot = getattr(settings, 'STATIC_ROOT', '%sbuild/static' % siteDir)

#         for cssDir in getattr(settings, 'GEOCAM_UTIL_PREPCSS_DIRS'):
#             fullDir = os.path.join(staticRoot, cssDir)
#             ret = os.chdir(fullDir)
#             if ret != 0:
#                 if verbosity > 1:
#                     print >> sys.stderr, ret
#             if verbosity > 1:
#                 print 'about to compass %s' % fullDir
#             dosys('compass clean ', verbosity)
#             dosys('compass compile ', verbosity)
#             if verbosity > 1:
#                 print 'done with compass'

        if compress:
            for compressFile in getattr(settings, 'GEOCAM_UTIL_COMPRESSCSS_FILES'):
                fullFile = os.path.join(staticRoot, compressFile)
                if verbosity > 1:
                    print 'about to compress %s' % fullFile
                dosys('yuglify %s' % fullFile, verbosity)
                if verbosity > 1:
                    print 'done compressing %s' % fullFile

