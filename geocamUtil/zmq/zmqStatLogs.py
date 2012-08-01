#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys
import logging
from collections import defaultdict
import datetime

from geocamUtil.zmq.util import LogParser

MSECS_PER_HOUR = 3600 * 1000000

def statLogs(opts, logPaths):
    i = 0
    for logPath in logPaths:
        count = defaultdict(int)
        print '=== compiling statistics on %s' % logPath
        logFile = open(logPath, 'rb')
        logStream = LogParser(logFile)
        for rec in logStream:
            bucket = int(rec.timestamp / MSECS_PER_HOUR)
            count[bucket] += 1
            i += 1

            if i % 10000 == 0:
                if not opts.quiet:
                    print 'processed %d records' % i

        buckets = sorted(count.keys())
        minBucket = buckets[0]
        maxBucket = buckets[-1]

        print
        for bucket in xrange(minBucket, maxBucket + 1):
            posixTimeStamp = bucket * 3600
            utcDt = datetime.datetime.utcfromtimestamp(posixTimeStamp)
            timeString = utcDt.strftime('%Y-%m-%d %H:00')
            if timeString.endswith('00:00'):
                print
            print '%s %6d' % (timeString, count[bucket])

        logFile.close()


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <messages.txt> <messages2.txt> ...')
    parser.add_option('-q', '--quiet',
                      action='store_true', default=False,
                      help='Reduce debug output')
    opts, args = parser.parse_args()
    if len(args) == 0:
        parser.error('expected at least 1 log file argument')
    logging.basicConfig(level=logging.DEBUG)

    statLogs(opts, args)


if __name__ == '__main__':
    main()
