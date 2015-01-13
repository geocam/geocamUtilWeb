# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os
import sys
import django

from optparse import make_option

from django.core.management.base import BaseCommand

from geocamUtil.management.commandUtil import getSiteDir, dosys
from geocamUtil import settings


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

