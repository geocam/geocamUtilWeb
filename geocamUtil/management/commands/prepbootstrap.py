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
Call grunt to compile bootstrap 4
"""
class Command(BaseCommand):
    help = 'Use grunt to compile css from sass in various directories.  Node, Ruby, grunt-cli, bundler must be installed.'

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))

        siteDir = getSiteDir()
        staticDir = getattr(settings, 'STATIC_ROOT', '%sbuild/static' % siteDir)
        bootstrapDir = os.path.join(staticDir, 'bootstrap')

        ret = os.chdir(bootstrapDir)
        if ret != 0:
            if verbosity > 1:
                print >> sys.stderr, ret
        if verbosity > 1:
            print 'about to grunt dist-css for bootstrap'
        dosys('grunt dist-css ', verbosity)
        if verbosity > 1:
            print 'done with grunt dist-css for bootstrap'

