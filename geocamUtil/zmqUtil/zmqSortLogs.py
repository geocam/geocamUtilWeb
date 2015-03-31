#!/usr/bin/env python
# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import logging

from geocamUtil.zmqUtil.util import LogParser


def sortLogs(opts, logPaths):
    outFiles = {}

    i = 0
    for logPath in logPaths:
        print '=== processing %s' % logPath
        logFile = open(logPath, 'rb')
        logStream = LogParser(logFile)
        for rec in logStream:
            topic, _body = rec.msg.split(':', 1)

            outFile = outFiles.get(topic)
            if outFile is None:
                outPath = '%s-zmq-messages.txt' % topic
                outFile = open(outPath, 'wb')
                outFiles[topic] = outFile

            rec.writeTo(outFile)
            i += 1

            if (i + 1) % 10000 == 0:
                print 'processed %d records, %d topics found so far' % (i + 1, len(outFiles))

        logFile.close()

    for outFile in outFiles.itervalues():
        outFile.close()


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <messages1.txt> <messages2.txt> ...')
    opts, args = parser.parse_args()
    if len(args) == 0:
        parser.error('expected at least 1 log file argument')
    logging.basicConfig(level=logging.DEBUG)

    sortLogs(opts, args)


if __name__ == '__main__':
    main()
