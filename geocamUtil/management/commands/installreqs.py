# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os

from django.core.management.base import NoArgsCommand

from geocamUtil.management import commandUtil

def dosys(cmd):
    print 'running:', cmd
    os.system(cmd)

class Command(NoArgsCommand):
    help = 'Use pip to install requirements found in management/requirements.txt'
    
    def handle_noargs(self, **options):
        if not commandUtil.getConfirmationUseStatus('installreqs', self.help):
            return

        needSudo = not os.environ.has_key('VIRTUAL_ENV')
        if needSudo:
            sudoStr = 'sudo '
        else:
            sudoStr = ''

        siteDir = commandUtil.getSiteDir()
        dosys('%spip install -r %smanagement/requirements.txt' % (sudoStr, siteDir))
