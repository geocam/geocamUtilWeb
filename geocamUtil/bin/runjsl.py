#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys
import os
import re
import tempfile

from geocamUtil.management.commandUtil import getSiteDir

STRIP_COMMENT = re.compile(r'#.*$')
CONFIG_FILE = os.path.join(getSiteDir(), 'management', 'jslrc.txt')
DEFAULT_FLAGS = '-nologo -nofilelisting'


def dosys(cmd):
    print 'running: %s' % cmd
    ret = os.system(cmd)
    if ret != 0:
        print 'warning: command exited with non-zero return value %d' % ret
    return ret


def runjsl(paths):
    if not paths:
        paths = ['.']

    # give helpful error message if jsl is not installed
    ret = os.system('jsl -help:conf > /dev/null')
    if ret != 0:
        print >> sys.stderr, "\nWARNING: can't run jsl command -- try http://www.javascriptlint.com/download.htm\n"
        sys.exit(1)

    # use <site>/management/jslrc.txt as rcfile if it exists
    print 'checking for jsl flags in %s' % CONFIG_FILE
    flags = DEFAULT_FLAGS
    if os.path.exists(CONFIG_FILE):
        flags += ' -conf %s' % CONFIG_FILE

    cmd = 'jsl %s' % flags
    for d in paths:
        d = os.path.relpath(d)
        fd, tempPath = tempfile.mkstemp('-runjslfiles.txt')
        os.close(fd)
        if os.path.isdir(d):
            dosys('find %s -name "*.js" | egrep -v "external|build|doc_src" > %s' % (d, tempPath))
            files = [f[:-1] for f in file(tempPath)]
            os.unlink(tempPath)
        else:
            files = [d]
        fileArgs = ' '.join(['-process %s' % f for f in files])
        dosys('%s %s' % (cmd, fileArgs))


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir1] [file2.js] ...')
    _opts, args = parser.parse_args()
    runjsl(args)

if __name__ == '__main__':
    main()
