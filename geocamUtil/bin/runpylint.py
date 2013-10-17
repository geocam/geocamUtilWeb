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
DEFAULT_FLAGS = '-i y -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"'


def dosys(cmd, verbosity):
    if verbosity > 1:
        print 'running: %s' % cmd
    ret = os.system(cmd)
    if verbosity > 1:
        if ret != 0:
            print 'warning: command exited with non-zero return value %d' % ret
    return ret


def runpylint(paths, verbosity=1):
    if verbosity > 0:
        print '### pylint'

    if not paths:
        paths = ['.']

    # give helpful error if pylint is not installed
    ret = os.system('pylint --help > /dev/null 2>&1')
    if ret != 0:
        print >> sys.stderr, "\nWARNING: can't run pylint command -- try 'pip install pylint'\n"
        sys.exit(1)

    # use <site>/management/pylintrc.txt as rcfile if it exists
    if verbosity > 1:
        print 'checking for pylint flags in %s' % CONFIG_FILE
    if os.path.exists(CONFIG_FILE):
        flags = '--rcfile %s' % CONFIG_FILE
    else:
        flags = DEFAULT_FLAGS

    cmd = 'pylint %s' % flags
    if verbosity > 2:
        xargsFlags = '--verbose'
    else:
        xargsFlags = ''
    for path in paths:
        path = os.path.relpath(path)
        if os.path.isdir(path):
            dosys('find %s -name "*.py" | egrep -v "external|attic|build/static" | xargs %s -n20 -d"\n" %s' % (path, xargsFlags, cmd), verbosity)
        else:
            dosys('%s %s' % (cmd, path), verbosity)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir1] [file2.py] ...')
    parser.add_option('-v', '--verbosity',
                      type='int',
                      default=1,
                      help='Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output')
    opts, args = parser.parse_args()
    runpylint(args, verbosity=opts.verbosity)

if __name__ == '__main__':
    main()
