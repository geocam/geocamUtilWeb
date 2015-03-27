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

import os
import tempfile
import unittest
import shutil
import time

from Builder import Builder


def catFiles(dst, srcs):
    srcStr = ' '.join(srcs)
    os.system('cat %s > %s' % (srcStr, dst))


def countLines(path):
    return len(file(path, 'r').read().splitlines())


class BuilderTest(unittest.TestCase):
    def getPath(self, name):
        return os.path.join(self.tmpDir, name)

    def setUp(self):
        # uncomment to get verbose debug output:
        # logging.basicConfig(level=logging.DEBUG, format='%(message)s')

        self.tmpDir = tempfile.mkdtemp('_BuilderTest')
        now = time.time()

        self.srcNames = ['1', '2', '3']
        self.srcPaths = [self.getPath(name) for name in self.srcNames]
        for name in self.srcNames:
            file(self.getPath(name), 'w').write(name + '\n')

        # make x appear to be written in the past so it needs to be built
        file(self.getPath('x'), 'w').write('x\n')
        os.utime(self.getPath('x'), (now - 1000, now - 1000))

        # make y appear to be written in the future so it is definitely up to date
        file(self.getPath('y'), 'w').write('y\n')
        os.utime(self.getPath('y'), (now + 1000, now + 1000))

    def tearDown(self):
        shutil.rmtree(self.tmpDir)

    def test_build(self):
        builder = Builder()

        dst = self.getPath('123')
        builder.applyRule(dst, self.srcPaths,
                          lambda: catFiles(dst, self.srcPaths))
        self.assert_(os.path.exists(dst))
        self.assertEquals(3, countLines(dst))

        dst = self.getPath('x')
        builder.applyRule(dst, self.srcPaths,
                          lambda: catFiles(dst, self.srcPaths))
        self.assertEquals(3, countLines(dst))

        self.assertEquals(2, builder.numRules)
        self.assertEquals(2, builder.numMade)

    def test_uptodate(self):
        builder = Builder()

        dst = self.getPath('y')
        builder.applyRule(dst, self.srcPaths,
                          lambda: catFiles(dst, self.srcPaths))
        self.assertEquals(1, countLines(dst))

        self.assertEquals(1, builder.numRules)
        self.assertEquals(0, builder.numMade)

if __name__ == '__main__':
    unittest.main()
