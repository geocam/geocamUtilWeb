# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import os

from django.test import TransactionTestCase
from django.core import management

from geocamUtil.management import commandUtil


def dosys(cmd):
    print 'running:', cmd
    os.system(cmd)


class CollectReqsTest(TransactionTestCase):
    def setUp(self):
        self.siteDir = commandUtil.getSiteDir()
        self.rfile = '%s/build/management/appRequirements.txt' % self.siteDir
        os.system('rm -f %s' % self.rfile)
        os.environ['TEST_SUPPRESS_STDERR'] = '1'

    def test_collect(self):
        management.call_command('collectreqs')
        self.assert_(os.path.exists(self.rfile))
        self.assertEquals(9, len(file(self.rfile, 'r').read().splitlines()))


class InstallReqsTest(TransactionTestCase):
    def tearDown(self):
        needSudo = 'VIRTUAL_ENV' not in os.environ
        if needSudo:
            sudoStr = 'sudo '
        else:
            sudoStr = ''
        dosys('%spip uninstall dutest electruth' % sudoStr)

    def test_install(self):
        management.call_command('installreqs')
        # test fails if the following imports fail
        import dutest as _
        import electruth as _


class PrepTemplatesTest(TransactionTestCase):
    def assertExists(self, f):
        self.assert_(os.path.exists(f))

    def setUp(self):
        self.siteDir = commandUtil.getSiteDir()
        self.ptDir = '%s/build/preptemplates/' % self.siteDir

    def tearDown(self):
        os.system('rm -rf %s' % self.ptDir)

    def test_preptemplates(self):
        management.call_command('preptemplates')
        self.assertExists('%sfoo.conf' % self.ptDir)
        self.assertExists('%sbar.conf' % self.ptDir)


class PrepAppsTest(TransactionTestCase):
    def setUp(self):
        self.siteDir = commandUtil.getSiteDir()
        self.ps1 = '%sbuild/app1/prepStatus.txt' % self.siteDir
        self.ps2 = '%sbuild/app2/prepStatus.txt' % self.siteDir

    def tearDown(self):
        os.system('rm -f %s' % self.ps1)
        os.system('rm -f %s' % self.ps2)

    def test_prep(self):
        management.call_command('prepapps')
        self.assert_(os.path.exists(self.ps1))
        self.assert_(os.path.exists(self.ps2))


class CollectMediaTest(TransactionTestCase):
    def setUp(self):
        self.siteDir = commandUtil.getSiteDir()
        self.bstaticDir = '%sbuild/static/' % self.siteDir

    def tearDown(self):
        os.system('rm -rf %s' % self.bstaticDir)

    def assertExists(self, f):
        self.assert_(os.path.exists(f))

    def test_collect(self):
        management.call_command('collectmedia')
        self.assertExists('%sapp1/js/app1.js' % self.bstaticDir)
        self.assertExists('%sapp2/js/app2.js' % self.bstaticDir)
        self.assertExists('%sexternal/js/lib1.js' % self.bstaticDir)
        self.assertExists('%sexternal/js/lib2.js' % self.bstaticDir)
        self.assertExists('%sexternal/js/sharedlib.js' % self.bstaticDir)
        self.assert_(not os.path.exists('%sshouldNotBeCollected.js' % self.bstaticDir))
