# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os

from django.test import TestCase
from django.core import management

def dosys(cmd):
    print 'running:', cmd
    os.system(cmd)

class CollectReqsTest(TestCase):
    def setUp(self):
        self.siteDir = os.path.dirname(os.path.abspath(__import__(os.environ['DJANGO_SETTINGS_MODULE']).__file__))
        self.rfile = '%s/build/management/appRequirements.txt' % self.siteDir
        os.system('rm -f %s' % self.rfile)
        os.environ['TEST_SUPPRESS_STDERR'] = '1'
    
    def test_collect(self):
        management.call_command('collectreqs')
        self.assert_(os.path.exists(self.rfile))
        self.assertEquals(9, len(file(self.rfile, 'r').read().splitlines()))

class InstallReqsTest(TestCase):
    def setUp(self):
        needSudo = not os.environ.has_key('VIRTUALENV')
        if needSudo:
            sudoStr = 'sudo '
        else:
            sudoStr = ''
        dosys('%spip uninstall dutest electruth' % sudoStr)
    
    def test_install(self):
        management.call_command('installreqs')
        # test fails if the following imports fail
        import dutest
        import electruth
