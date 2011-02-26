# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from optparse import make_option
from django.core.management.base import NoArgsCommand, CommandError

import os

def dosys(cmd):
    print 'running:', cmd
    os.system(cmd)

class Command(NoArgsCommand):
    help = 'Uses pip to install requirements found in management/requirements.txt'
    
    def handle_noargs(self, **options):
        needSudo = not os.environ.has_key('VIRTUALENV')
        if needSudo:
            sudoStr = 'sudo '
        else:
            sudoStr = ''

        siteDir = os.path.dirname(os.path.abspath(__import__(os.environ['DJANGO_SETTINGS_MODULE']).__file__))

        dosys('%spip install -r %s/management/requirements.txt' % (sudoStr, siteDir))
