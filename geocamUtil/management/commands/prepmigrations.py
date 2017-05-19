# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from geocamUtil.management import commandUtil
from django.core import management
from django.conf import settings
import traceback

class Command(commandUtil.PathCommand):
    help = 'Execute manage.py makemigrations for each app in the site'

    def isValid(self, name):
        for exclude in settings.GEOCAM_UTIL_PREP_EXLUSION_APPS:
            if name.startswith(exclude):
                return False
            
        return True

    def handleImportPaths(self, impPaths, options):
        for appName in reversed(impPaths):
            if not appName.startswith('django'):
                if self.isValid(appName):
                    try:
                        print "Migrating %s" % appName
                        management.call_command('makemigrations', appName)
                    except:
                        traceback.print_exc()
                        pass
