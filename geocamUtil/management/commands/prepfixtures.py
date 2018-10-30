# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import traceback
from geocamUtil.management import commandUtil
from django.core import management
from django.core.management.base import CommandError


class Command(commandUtil.PathCommand):
    help = 'Execute manage.py loaddata for each app in the site'

    def handleImportPaths(self, impPaths, options):
        for appName in reversed(impPaths):
            print "Loading initial data for %s" % appName
            try:
                filename = '%s_initial_data.json' % appName
                management.call_command('loaddata', filename, app=appName)
            except CommandError as ce:
                if not ce.message.startswith("No fixture named"):
                    print '######## PROBLEM LOADING INITIAL DATA %s ####' % filename
                    traceback.print_exc(ce)
                    print '######## END PROBLEM LOADING INITIAL DATA %s ####' % filename
                pass
            except Exception as e:
                print '######## PROBLEM LOADING INITIAL DATA %s ####' % filename
                traceback.print_exc(e)
                print '######## END PROBLEM LOADING INITIAL DATA %s ####' % filename
                pass


