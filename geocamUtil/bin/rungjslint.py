#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys
import os

from geocamUtil.management.commandUtil import getSiteDir, lintignore

CONFIG_FILE = os.path.join(getSiteDir(), 'management', 'gjslintFlags.txt')
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_FLAGS = '--unix_mode'


def dosys(cmd, verbosity):
    if verbosity > 1:
        print 'running: %s' % cmd
    ret = os.system(cmd)
    if verbosity > 1:
        if ret != 0:
            print 'warning: command exited with non-zero return value %d' % ret
    return ret


def rungjslint(paths, verbosity=1):
    if verbosity > 0:
        print '### gjslint'

    if not paths:
        paths = ['.']

    # give helpful error message if gjslint is not installed
    ret = os.system('gjslint > /dev/null')
    if ret != 0:
        print >> sys.stderr, "\nWARNING: can't run gjslint command -- try 'pip install http://closure-linter.googlecode.com/files/closure_linter-latest.tar.gz'"
        sys.exit(1)

    # use rcfile if it exists
    if verbosity > 1:
        print 'checking for gjslint flags in %s' % CONFIG_FILE
    flags = DEFAULT_FLAGS
    if os.path.exists(CONFIG_FILE):
        flags += ' --flagfile %s' % CONFIG_FILE

    cmd = 'gjslint %s' % flags
    for d in paths:
        if verbosity > 2:
            print 'directory:', d
        d = os.path.relpath(d)
        if os.path.isdir(d):
            pathsText = lintignore(os.popen('find %s -name "*.js"' % d).read())
            files = pathsText.splitlines()
        else:
            files = [d]
        if files:
            fileArgs = ' '.join(files)
            dosys('%s %s' % (cmd, fileArgs), verbosity)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir1] [file2.js] ...')
    parser.add_option('-v', '--verbosity',
                      type='int',
                      default=1,
                      help='Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output')
    opts, args = parser.parse_args()
    rungjslint(args, verbosity=opts.verbosity)

if __name__ == '__main__':
    main()
