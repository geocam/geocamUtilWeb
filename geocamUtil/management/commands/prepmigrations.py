# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from geocamUtil.management import commandUtil
from django.core import management

class Command(commandUtil.PathCommand):
    help = 'Execute manage.py makemigrations for each app in the site'

    def handleImportPaths(self, impPaths, options):
        for appName in reversed(impPaths):
            if not appName.startswith('django'):
                management.call_command('makemigrations', appName)
