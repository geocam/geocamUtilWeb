#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys
import os

from geocamUtil.management.commandUtil import getSiteDir

CONFIG_FILE = os.path.join(getSiteDir(), 'management', 'pylintrc.txt')
DEFAULT_FLAGS = '-i y -r n -f parseable'


def dosys(cmd):
    print 'running: %s' % cmd
    ret = os.system(cmd)
    if ret != 0:
        print 'warning: command exited with non-zero return value %d' % ret
    return ret


def runpylint(paths):
    if not paths:
        paths = ['.']

    # give helpful error if pylint is not installed
    ret = os.system('pylint --help > /dev/null')
    if ret != 0:
        print >> sys.stderr, "\nWARNING: can't run pylint command -- try 'pip install pylint'\n"
        sys.exit(1)

    # use <site>/management/pylintrc.txt as rcfile if it exists
    print 'checking for pylint flags in %s' % CONFIG_FILE
    if os.path.exists(CONFIG_FILE):
        flags = '--rcfile %s' % CONFIG_FILE
    else:
        flags = DEFAULT_FLAGS

    cmd = 'pylint %s' % flags
    for path in paths:
        path = os.path.relpath(path)
        if os.path.isdir(path):
            dosys('find %s -name "*.py" | xargs -n 50 %s' % (path, cmd))
        else:
            dosys('%s %s' % (cmd, path))


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir1] [file2.py] ...')
    _opts, args = parser.parse_args()
    runpylint(args)

if __name__ == '__main__':
    main()
