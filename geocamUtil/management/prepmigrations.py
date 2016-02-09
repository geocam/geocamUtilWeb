# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import logging

from geocamUtil.management import commandUtil
from django.core import management


class Command(commandUtil.PathCommand):
    help = 'Execute management/appCommands/makemigrations.py for each app in the site'

    def handleImportPaths(self, impPaths, options):
        for appName in impPaths:
            theCommand = 'makemigrations %s' % appName
            management.call_command(theCommand)
