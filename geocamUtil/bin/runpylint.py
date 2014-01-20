#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys
import os

from geocamUtil.management.commandUtil import getSiteDir, lintignore, pipeToCommand

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

    exitCode = 0
    for path in paths:
        path = os.path.relpath(path)
        if os.path.isdir(path):
            pathsText = lintignore(os.popen('find %s -name "*.py"' % path).read())
            ret = pipeToCommand('xargs %s --no-run-if-empty -n20 -d"\n" %s' % (xargsFlags, cmd),
                                pathsText, verbosity)
            if ret != 0:
                exitCode = 1
        else:
            ret = dosys('%s %s' % (cmd, path), verbosity)
            if ret != 0:
                exitCode = 1

    return exitCode


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir1] [file2.py] ...')
    parser.add_option('-v', '--verbosity',
                      type='int',
                      default=1,
                      help='Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output')
    opts, args = parser.parse_args()
    exitCode = runpylint(args, verbosity=opts.verbosity)
    sys.exit(exitCode)


if __name__ == '__main__':
    main()
