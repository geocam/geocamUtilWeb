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


def runpep8(dirs):
    for d in dirs:
        d = os.path.relpath(d)
        cmd = 'pep8 --ignore=E501 --show-pep8 --repeat'
        if os.path.isdir(d):
            dosys('find %s -name "*.py" | xargs -n 50 %s' % (d, cmd))
        else:
            dosys('%s %s' % (cmd, d))

def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir1] [file2.py] ...')
    opts, args = parser.parse_args()
    if len(args) == 0:
        dirs = ['.']
    else:
        dirs = args
    runpep8(dirs)

if __name__ == '__main__':
    main()
