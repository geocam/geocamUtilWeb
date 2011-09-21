#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys
import os
import re

from geocamUtil.management.commandUtil import getSiteDir

STRIP_COMMENT = re.compile(r'#.*$')
CONFIG_FILE = os.path.join(getSiteDir(), 'management', 'pep8Flags.txt')
DEFAULT_FLAGS = '--ignore=E501 --show-pep8 --repeat'


def dosys(cmd):
    print 'running: %s' % cmd
    ret = os.system(cmd)
    if ret != 0:
        print 'warning: command exited with non-zero return value %d' % ret
    return ret


def readFlags(path):
    f = file(path, 'r')
    flags = []
    for line in f:
        line = re.sub(STRIP_COMMENT, '', line)
        line = line.strip()
        if line:
            flags.append(line)
    return ' '.join(flags)


def runpep8(paths):
    if not paths:
        paths = ['.']

    # give helpful error message if pep8 is not installed
    ret = os.system('pep8 --help > /dev/null')
    if ret != 0:
        print >> sys.stderr, "\nWARNING: can't run pep8 command -- try 'pip install pep8'\n"
        sys.exit(1)

    # extract flags from <site>/management/pep8Flags.txt if it exists
    print 'checking for pep8 flags in %s' % CONFIG_FILE
    if os.path.exists(CONFIG_FILE):
        flags = readFlags(CONFIG_FILE)
    else:
        flags = DEFAULT_FLAGS

    for d in paths:
        d = os.path.relpath(d)
        cmd = 'pep8 %s' % flags
        if os.path.isdir(d):
            dosys('find %s -name "*.py" | xargs -n 50 %s' % (d, cmd))
        else:
            dosys('%s %s' % (cmd, d))


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir1] [file2.py] ...')
    _opts, args = parser.parse_args()
    runpep8(args)

if __name__ == '__main__':
    main()
