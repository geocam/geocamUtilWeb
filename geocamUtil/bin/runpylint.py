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

from geocamUtil.management.commandUtil import getSiteDir, lintignore, pipeToCommand

CONFIG_FILE = os.path.join(getSiteDir(), 'management', 'pylintrc.txt')
DEFAULT_FLAGS = '-i y -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"'


def dosys(cmd, verbosity):
    if verbosity > 1:
        print >> sys.stderr, 'running: %s' % cmd
    ret = os.system(cmd)
    if verbosity > 1:
        if ret != 0:
            print >> sys.stderr, 'warning: command exited with non-zero return value %d' % ret
    return ret


def runpylint(paths, verbosity=1):
    if verbosity > 0:
        print >> sys.stderr, '### pylint'

    if not paths:
        paths = ['.']

    # give helpful error if pylint is not installed
    ret = os.system('pylint --help > /dev/null 2>&1')
    if ret != 0:
        print >> sys.stderr, "\nWARNING: can't run pylint command -- try 'pip install pylint'\n"
        sys.exit(1)

    # use <site>/management/pylintrc.txt as rcfile if it exists
    if verbosity > 1:
        print >> sys.stderr, 'checking for pylint flags in %s' % CONFIG_FILE
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
            findCmd = 'find %s -name "*.py"' % path
            rawPathsText = os.popen(findCmd).read()
            pathsText = lintignore(rawPathsText)
            if verbosity > 1:
                print >> sys.stderr, 'findCmd:', findCmd
                print >> sys.stderr, 'rawPathsText:\n' + rawPathsText
                print >> sys.stderr, '\npathsText:\n' + pathsText
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
