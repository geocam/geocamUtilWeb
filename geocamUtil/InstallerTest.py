# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import unittest
import os
import shutil
import tempfile

from Installer import Installer


def touchFile(path):
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d)
    file(path, 'w').close()


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        print self.dir
        touchFile('%s/app1/ab/a.txt' % self.dir)
        touchFile('%s/app2/ab/b.txt' % self.dir)
        touchFile('%s/app1/xy/x.txt' % self.dir)
        touchFile('%s/app2/xy/y.txt' % self.dir)
        self.inst = Installer()

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_first(self):
        self.inst.installRecurseGlob(r'%s/app[12]/*' % self.dir,
                                     '%s/both' % self.dir)
        self.assert_(os.path.exists('%s/both/ab/a.txt' % self.dir))
        self.assert_(os.path.exists('%s/both/ab/b.txt' % self.dir))
        self.assert_(os.path.exists('%s/both/xy/x.txt' % self.dir))
        self.assert_(os.path.exists('%s/both/xy/y.txt' % self.dir))

if __name__ == '__main__':
    unittest.main()
