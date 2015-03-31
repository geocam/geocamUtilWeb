#!/usr/bin/env python
# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import logging
import sys
import time


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog testMessages.txt')
    _opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error('expected exactly 1 arg')
    msgFile = args[0]
    logging.basicConfig(level=logging.DEBUG)

    lines = list(open(msgFile, 'r'))
    while 1:
        for line in lines:
            sys.stdout.write(line)
            sys.stdout.flush()
            time.sleep(0.5)


if __name__ == '__main__':
    main()
