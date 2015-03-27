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

import sys
import os
import stat
import errno
import traceback
import logging


class Builder(object):
    def __init__(self):
        self.numMade = 0
        self.numRules = 0
        self.logger = logging.getLogger('geocamUtil.Builder')

    def applyRule(self, dst, srcs, func):
        self.numRules += 1

        try:
            dstStat = os.stat(dst)
        except OSError, e:
            if e.errno == errno.ENOENT:
                dstStat = None
            else:
                raise

        if dstStat:
            dstMode = dstStat[stat.ST_MODE]
            if stat.S_ISLNK(dstMode) or stat.S_ISDIR(dstMode):
                # assume symlinks and directories are up to date
                self.logger.debug('builder: %s is symlink or directory, no rebuild needed' % dst)
                rebuild = False
            else:
                dstTime = dstStat[stat.ST_MTIME]
                maxSrcTime = 0
                for src in srcs:
                    try:
                        srcTime = os.stat(src)[stat.ST_MTIME]
                    except OSError, e:
                        traceback.print_exc()
                        self.logger.error('[could not stat source file %s in rule to generate %s]'
                                          % (src, dst))
                        sys.exit(1)
                    maxSrcTime = max(maxSrcTime, srcTime)
                self.logger.debug('builder: srcs=%s maxSrcTime=%s dstTime=%s'
                                  % (srcs, maxSrcTime, dstTime))
                rebuild = (maxSrcTime > dstTime)
        else:
            rebuild = True

        if rebuild:
            self.logger.debug('[building: %s]' % dst)
            func()
            self.numMade += 1
        else:
            self.logger.debug('[up to date: %s]' % dst)

    def finish(self):
        self.logger.info('builder: %d of %d files were up to date' % (self.numRules - self.numMade, self.numRules))
