#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os

from geocamUtil import settings


def dosys(cmd):
    print 'running: %s' % cmd
    ret = os.system(cmd)
    if ret != 0:
        print 'warning: command exited with non-zero return value %d' % ret
    return ret


def runpylint(paths):
    pylintrcPath = os.path.join(settings.CHECKOUT_DIR, 'management', 'pylintrc.txt')
    if os.path.exists(pylintrcPath):
        pylintrcFlag = ' --rcfile %s ' % pylintrcPath
    else:
        pylintrcFlag = ''
    cmd = 'pylint -i y -r n -f parseable %s' % pylintrcFlag
    for path in paths:
        path = os.path.relpath(path)
        if os.path.isdir(path):
            dosys('find %s -name "*.py" | xargs -n 50 %s' % (path, cmd))
        else:
            dosys('%s %s' % (cmd, path))


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir1] [file2.py] ...')
    opts, args = parser.parse_args()
    if len(args) == 0:
        paths = ['.']
    else:
        paths = args
    runpylint(paths)

if __name__ == '__main__':
    main()
