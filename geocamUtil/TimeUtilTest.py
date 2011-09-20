# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import unittest
import pytz
import datetime

from geocamUtil.TimeUtil import getTimeShort, stringToLocalDT


def equalUpToSeconds(a, b):
    return (a.replace(second=0, microsecond=0)
            == b.replace(second=0, microsecond=0))


class TimeUtilTest(unittest.TestCase):
    def parseCase(self, inp, now, intervalStart, correct):
        nowDT = datetime.datetime.strptime(now, '%Y-%m-%d-%H:%M')
        correctDT = datetime.datetime.strptime(correct, '%Y-%m-%d-%H:%M')
        resultDT = stringToLocalDT(inp, intervalStart, nowDT)
        self.assert_(equalUpToSeconds(resultDT, correctDT))

    def test_stringToLocalDT(self):
        self.parseCase(inp='2009-2-4-9:48',
                       now='2009-02-04-09:48',
                       intervalStart=True,
                       correct='2009-02-04-09:48')
        self.parseCase(inp='2-4-9:48',
                       now='2009-02-04-09:48',
                       intervalStart=True,
                       correct='2009-02-04-09:48')
        self.parseCase(inp='9:48',
                       now='2009-02-04-09:48',
                       intervalStart=True,
                       correct='2009-02-04-09:48')

        self.parseCase(inp='2009-2-4',
                       now='2009-02-04-09:48',
                       intervalStart=True,
                       correct='2009-02-04-00:00')
        self.parseCase(inp='2009-2-4',
                       now='2009-02-04-09:48',
                       intervalStart=False,
                       correct='2009-02-04-23:59')

        self.parseCase(inp='2009',
                       now='2009-02-04-09:48',
                       intervalStart=True,
                       correct='2009-01-01-00:00')
        self.parseCase(inp='2009',
                       now='2009-02-04-09:48',
                       intervalStart=False,
                       correct='2009-12-31-23:59')

    def getTimeShortCase(self, timestamp, now, tzcode, correct):
        fmt = '%Y-%m-%d-%H:%M:%S'
        timestampDt = datetime.datetime.strptime(timestamp, fmt)
        nowDt = datetime.datetime.strptime(now, fmt)
        result = getTimeShort(timestampDt,
                              tz=pytz.timezone(tzcode),
                              now=nowDt)
        self.assertEqual(result, correct)

    def test_getTimeShort01(self):
        self.getTimeShortCase(timestamp='2011-08-30-10:08:37',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='1 minute ago')

    def test_getTimeShort02(self):
        self.getTimeShortCase(timestamp='2011-08-30-10:06:38',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='1 minute ago')

    def test_getTimeShort03(self):
        self.getTimeShortCase(timestamp='2011-08-30-10:06:36',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='2 minutes ago')

    def test_getTimeShort04(self):
        self.getTimeShortCase(timestamp='2011-08-30-09:09:00',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='59 minutes ago')

    def test_getTimeShort05(self):
        self.getTimeShortCase(timestamp='2011-08-30-09:07:36',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='1 hour ago')

    def test_getTimeShort06(self):
        self.getTimeShortCase(timestamp='2011-08-29-10:09:00',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='23 hours ago')

    def test_getTimeShort07(self):
        self.getTimeShortCase(timestamp='2011-08-29-10:07:00',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='Yesterday')

    def test_getTimeShort08(self):
        self.getTimeShortCase(timestamp='2011-08-28-10:07:00',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='2 days ago')

    def test_getTimeShort09(self):
        self.getTimeShortCase(timestamp='2011-08-26-10:07:00',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='4 days ago')

    def test_getTimeShort10(self):
        self.getTimeShortCase(timestamp='2011-08-25-10:07:00',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='Aug 25')

    def test_getTimeShort11(self):
        self.getTimeShortCase(timestamp='2010-12-25-10:07:00',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='2010-12-25')

    def test_getTimeShort12(self):
        self.getTimeShortCase(timestamp='2010-12-25-03:07:00',
                              now='2011-08-30-10:08:37',
                              tzcode='US/Central',
                              correct='2010-12-24')

if __name__ == '__main__':
    unittest.main()
