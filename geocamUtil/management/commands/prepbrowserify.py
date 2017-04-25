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
Could not get django-pipeline-browserify to work, so instead we are calling browserify from command line.
This requires browserify to be installed with node, and any included dependencies also to be installed with node.
For reference:
https://marionette.gitbooks.io/marionette-guides/content/en/getting_started/installing_marionette.html

example command
browserify build/static/xgds_map_server/js/browserify.js -t node-underscorify -d -o build/static/backbone_marionette_browserify.js

"""
class Command(BaseCommand):
    help = 'Use browserify to make pure node libraries that use require available in the browser window'

    def getCommandPrefix(self):
        fullCommand = 'browserify -t node-underscorify '
        if settings.DEBUG:
            fullCommand += '-d '
        return fullCommand

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))

        appsRoot = os.path.join(getattr(settings, 'PROJ_ROOT'), 'apps')
        siteDir = getSiteDir()
        staticRoot = getattr(settings, 'STATIC_ROOT', '%sbuild/static' % siteDir)


        fullCommand = self.getCommandPrefix()
        for entry in getattr(settings, 'XGDS_BROWSERIFY'):
            for source_filename in entry['source_filenames']:
                fullCommand += os.path.join(appsRoot, source_filename) + ' '
            
            fullCommand += '-o ' + os.path.join(staticRoot, entry['output_filename'])
            
            if verbosity > 1:
                print 'about to browserify %s' % entry['output_filename']
            dosys(fullCommand, verbosity)
            if verbosity > 1:
                print 'done with browserify'
            
            fullCommand = self.getCommandPrefix()


