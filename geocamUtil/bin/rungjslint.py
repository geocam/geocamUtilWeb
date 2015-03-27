#!/usr/bin/env python
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

from geocamUtil.management.commandUtil import getSiteDir, lintignore

CONFIG_FILE = os.path.join(getSiteDir(), 'management', 'gjslintFlags.txt')
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_FLAGS = '--unix_mode'


def dosys(cmd, verbosity):
    if verbosity > 1:
        print >> sys.stderr, 'running: %s' % cmd
    ret = os.system(cmd)
    if verbosity > 1:
        if ret != 0:
            print >> sys.stderr, 'warning: command exited with non-zero return value %d' % ret
    return ret


def rungjslint(paths, verbosity=1):
    if verbosity > 0:
        print >> sys.stderr, '### gjslint'

    if not paths:
        paths = ['.']

    # give helpful error message if gjslint is not installed
    ret = os.system('gjslint > /dev/null')
    if ret != 0:
        print >> sys.stderr, "\nWARNING: can't run gjslint command -- try 'pip install http://closure-linter.googlecode.com/files/closure_linter-latest.tar.gz'"
        sys.exit(1)

    # use rcfile if it exists
    if verbosity > 1:
        print >> sys.stderr, 'checking for gjslint flags in %s' % CONFIG_FILE
    flags = DEFAULT_FLAGS
    if os.path.exists(CONFIG_FILE):
        flags += ' --flagfile %s' % CONFIG_FILE

    exitCode = 0
    cmd = 'gjslint %s' % flags
    for d in paths:
        if verbosity > 2:
            print >> sys.stderr, 'directory:', d
        d = os.path.relpath(d)
        if os.path.isdir(d):
            pathsText = lintignore(os.popen('find %s -name "*.js"' % d).read())
            files = pathsText.splitlines()
        else:
            files = [d]
        if files:
            fileArgs = ' '.join(files)
            ret = dosys('%s %s' % (cmd, fileArgs), verbosity)
            if ret != 0:
                exitCode = 1

    return exitCode


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir1] [file2.js] ...')
    parser.add_option('-v', '--verbosity',
                      type='int',
                      default=1,
                      help='Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output')
    opts, args = parser.parse_args()
    exitCode = rungjslint(args, verbosity=opts.verbosity)
    sys.exit(exitCode)


if __name__ == '__main__':
    main()
