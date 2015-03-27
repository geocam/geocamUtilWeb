# __BEGIN_LICENSE__
#Copyright © 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
#
#The xGDS platform is licensed under the Apache License, Version 2.0 
#(the "License"); you may not use this file except in compliance with the License. 
#You may obtain a copy of the License at 
#http://www.apache.org/licenses/LICENSE-2.0.
#
#Unless required by applicable law or agreed to in writing, software distributed 
#under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
#CONDITIONS OF ANY KIND, either express or implied. See the License for the 
#specific language governing permissions and limitations under the License.
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
