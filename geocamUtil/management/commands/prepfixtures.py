# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from geocamUtil.management import commandUtil
from django.core import management
from django.conf import settings

class Command(commandUtil.PathCommand):
    help = 'Execute manage.py loaddata for each app in the site'

    def handleImportPaths(self, impPaths, options):
        for appName in reversed(impPaths):
            print "Loading initial data for %s" % appName
            try:
                path = '%s/initial_data.json' % appName
                management.call_command('loaddata', path, app=appName)
            except:
                pass

