# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys
import os
import stat
import errno
import traceback
import logging


class Builder:
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
