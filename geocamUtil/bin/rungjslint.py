#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys
import os
import tempfile

from geocamUtil.management.commandUtil import getSiteDir

CONFIG_FILE = os.path.join(getSiteDir(), 'management', 'gjslintFlags.txt')
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_FLAGS = '--unix_mode'


def dosys(cmd):
    print 'running: %s' % cmd
    ret = os.system(cmd)
    if ret != 0:
        print 'warning: command exited with non-zero return value %d' % ret
    return ret


def rungjslint(paths):
    if not paths:
        paths = ['.']

    # give helpful error message if jsl is not installed
    ret = os.system('gjslint > /dev/null')
    if ret != 0:
        print >> sys.stderr, "\nWARNING: can't run gjslint command -- find it at https://developers.google.com/closure/utilities/\n"
        sys.exit(1)

    # use rcfile if it exists
    print 'checking for gjslint flags in %s' % CONFIG_FILE
    flags = DEFAULT_FLAGS
    if os.path.exists(CONFIG_FILE):
        flags += ' --flagfile %s' % CONFIG_FILE

    cmd = 'gjslint %s' % flags
    for d in paths:
        print 'd:', d
        d = os.path.relpath(d)
        fd, tempPath = tempfile.mkstemp('-rungjslintfiles.txt')
        os.close(fd)
        if os.path.isdir(d):
            dosys('find %s -name "*.js" | egrep -v "external|build|doc_src|attic" > %s' % (d, tempPath))
            files = [f[:-1] for f in file(tempPath)]
            os.unlink(tempPath)
        else:
            files = [d]
        fileArgs = ' '.join(files)
        dosys('%s %s' % (cmd, fileArgs))


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir1] [file2.js] ...')
    _opts, args = parser.parse_args()
    rungjslint(args)

if __name__ == '__main__':
    main()
