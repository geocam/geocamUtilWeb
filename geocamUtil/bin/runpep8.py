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


def runpep8(root):
    root = os.path.relpath(root)
    dosys('find %s -name "*.py" | xargs -n 50 pep8 --ignore=E501 --show-pep8 --repeat' % root)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog [dir]')
    opts, args = parser.parse_args()
    if len(args) == 0:
        root = '.'
    elif len(args) == 1:
        root = args[0]
    else:
        parser.error('expected 0 or 1 args')
    runpep8(root)

if __name__ == '__main__':
    main()
