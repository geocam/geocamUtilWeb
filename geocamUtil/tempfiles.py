# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os
import time
import random
import shutil
from glob import glob
import traceback
import sys

from geocamUtil import FileUtil
from geocamUtil import settings


def getTempName(prefix, suffix=''):
    return '%s/%s-%s-%s%s' % (settings.TMP_DIR,
                              prefix,
                              time.strftime('%Y-%m-%d-%H%M'),
                              '%04x' % random.getrandbits(16),
                              suffix)


def deleteStaleFiles():
    files = glob('%s/*' % settings.TMP_DIR)
    now = time.time()
    for f in files:
        if (now - os.stat(f).st_ctime > settings.GEOCAM_UTIL_DELETE_TMP_FILE_WAIT_SECONDS
            and not f.endswith('/README.txt')):
            try:
                os.unlink(f)
            except OSError:
                traceback.print_exc()
                print >> sys.stderr, '[tempfiles.deleteStaleFiles: could not unlink %s]' % f


def makeTempDir(prefix):
    d = getTempName(prefix)
    if not os.path.exists(settings.TMP_DIR):
        FileUtil.mkdirP(settings.TMP_DIR)
        os.system('chmod go+rw %s' % settings.TMP_DIR)
    deleteStaleFiles()
    FileUtil.mkdirP(d)
    return d


def initZipDir(prefix):
    return makeTempDir(prefix)


def finishZipDir(zipDir):
    zipFile = '%s.zip' % zipDir
    oldDir = os.getcwd()
    os.chdir(os.path.dirname(settings.TMP_DIR))
    os.system('zip -r %s %s' % (zipFile, os.path.basename(zipDir)))
    os.chdir(oldDir)
    shutil.rmtree(zipDir)
    return zipFile
