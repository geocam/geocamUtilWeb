#!/usr/bin/env python

"""
A test file source to write files to be published by filePublisher.py.
"""

import logging
import os
import time


def dosys(cmd):
    print cmd
    os.system(cmd)


def testFileSource(opts, args):
    i = 0
    while 1:
        for f in args:
            _name, ext = os.path.splitext(f)
            dosys('cp %s %s/%06d%s' % (f, opts.output, i, ext))
            i += 1
            time.sleep(opts.period)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog OPTIONS <FILES>\n' + __doc__)
    parser.add_option('-o', '--output',
                      default='.',
                      help='Directory to write files to [%default]')
    parser.add_option('-p', '--period',
                      type='float', default=1.0,
                      help='Period between writing new files (seconds) [%default]')
    opts, args = parser.parse_args()
    if not args:
        parser.error('expected file arguments')

    logging.basicConfig(level=logging.DEBUG)

    testFileSource(opts, args)


if __name__ == '__main__':
    main()
