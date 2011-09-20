# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os

from django.test import TestCase
from django.core import management

from geocamUtil.management import commandUtil


def dosys(cmd):
    print 'running:', cmd
    os.system(cmd)


class CollectReqsTest(TestCase):
    def setUp(self):
        self.siteDir = commandUtil.getSiteDir()
        self.rfile = '%s/build/management/appRequirements.txt' % self.siteDir
        os.system('rm -f %s' % self.rfile)
        os.environ['TEST_SUPPRESS_STDERR'] = '1'

    def test_collect(self):
        management.call_command('collectreqs')
        self.assert_(os.path.exists(self.rfile))
        self.assertEquals(9, len(file(self.rfile, 'r').read().splitlines()))


class InstallReqsTest(TestCase):
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


class PrepTemplatesTest(TestCase):
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


class PrepAppsTest(TestCase):
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


class CollectMediaTest(TestCase):
    def setUp(self):
        self.siteDir = commandUtil.getSiteDir()
        self.bmediaDir = '%sbuild/media/' % self.siteDir

    def tearDown(self):
        os.system('rm -rf %s' % self.bmediaDir)

    def assertExists(self, f):
        self.assert_(os.path.exists(f))

    def test_collect(self):
        management.call_command('collectmedia')
        self.assertExists('%sapp1/js/app1.js' % self.bmediaDir)
        self.assertExists('%sapp2/js/app2.js' % self.bmediaDir)
        self.assertExists('%sexternal/js/lib1.js' % self.bmediaDir)
        self.assertExists('%sexternal/js/lib2.js' % self.bmediaDir)
        self.assertExists('%sexternal/js/sharedlib.js' % self.bmediaDir)
        self.assert_(not os.path.exists('%sshouldNotBeCollected.js' % self.bmediaDir))
