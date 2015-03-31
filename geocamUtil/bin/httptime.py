#!/usr/bin/env python
# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

"""
Hack emulation of NTP-like functionality if your firewall blocks UDP but
you have the ability to connect to a web server with an accurate
clock. We request an arbitrary page from the web server, extract the
current time from the HTTP 'Date' header, and set the local time to that
value. There is no correction for estimated network delay. This is less
accurate and less bandwidth-efficient than real NTP, but might be more
reliable.

Typically, you might call this script as a daily cron job in root's
crontab (setting your clock requires superuser privileges).  This is an
example line you might append to the crontab to update the time at
2:05 AM every morning (use 'sudo crontab -e' to open root's crontab in
an editor):

5 2 * * * /full/path/to/httptime.py 2>&1 > /dev/null
"""

import os
import urllib2
import re
import datetime
import logging

DATE_HEADER_FORMATS = ['%a, %d %b %Y %H:%M:%S %Z' # Thu, 19 Feb 2015 01:54:56 GMT
                       ]

def dosys(cmd):
    logging.info('running: %s', cmd)
    ret = os.system(cmd)
    if ret != 0:
        logging.warn('  command exited with non-zero return value %s', ret)
    return ret


def getDateTime(url):
    logging.info('fetching time from server at %s', url)
    conn = urllib2.urlopen(url)
    dateStr = conn.info().getheader('Date')
    conn.close()
    if not dateStr:
        raise ValueError('HTTP response "Date" header not found')
    if not ('GMT' in dateStr or 'UTC' in dateStr):
        raise ValueError('HTTP response "Date" header does not appear to be UTC')
    for fmt in DATE_HEADER_FORMATS:
        try:
            return datetime.datetime.strptime(dateStr, fmt)
        except ValueError:
            pass
    raise RuntimeError('HTTP response "Date" header does not match any of the known datetime formats')


def setDateTime(dt):
    dateArg = dt.strftime('%m%d%H%M%Y.%S')
    logging.info('server time is %s UTC', dt)
    logging.info('setting time on local host')
    dosys('date -u %s' % dateArg)
    logging.info('done')


def httptime(opts):
    dt = getDateTime(opts.url)
    setDateTime(dt)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog OPTIONS\n' + __doc__.rstrip())
    parser.add_option('-u', '--url',
                      default='http://www.google.com/',
                      help='URL to fetch time from [%default]')
    opts, args = parser.parse_args()
    if args:
        parser.error('expected no args')
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    httptime(opts)


if __name__ == '__main__':
    main()
