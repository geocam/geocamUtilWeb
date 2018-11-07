# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import copy
import time
import datetime
import calendar
import re

import iso8601
try:
    import pytz
except ImportError:
    # older functions don't use pytz so for backward compatibility
    # with older installs we shouldn't require it
    pass


def utcToTimeZone(dt, tz):
    # returns localized datetime in given timezone
    if isinstance(tz, (str, unicode)):
        tz = pytz.timezone(tz)
    mydt = copy.copy(dt)
    return mydt.replace(tzinfo=pytz.utc).astimezone(tz)


def timeZoneToUtc(dt):
    # returns UTC datetime 
    return dt.astimezone(pytz.utc)


def localDateTimeToPosix(localDT):
    return time.mktime(localDT.timetuple()) + 1e-6 * localDT.microsecond


def utcDateTimeToPosix(utcDT):
    return calendar.timegm(utcDT.timetuple()) + 1e-6 * utcDT.microsecond


def posixToUtcDateTime(posixTime):
    return datetime.datetime.utcfromtimestamp(posixTime)


def posixToLocalDateTime(posixTime):
    return datetime.datetime.fromtimestamp(posixTime)


def localToUtcTime(localDT):
    """for the record, this is ridiculous"""
    posixTime = localDateTimeToPosix(localDT)
    utcDT = posixToUtcDateTime(posixTime)
    return utcDT


def utcToLocalTime(utcDT):
    """let's see how many time-related modules we can import"""
    posixTime = utcDateTimeToPosix(utcDT)
    localDT = posixToLocalDateTime(posixTime)
    return localDT


def utcNow():
    return posixToUtcDateTime(time.time())


def formatUtcTimeAsAbbreviatedLocalTime(utcDT):
    try:
        utcDT.timetuple()
    except AttributeError:
        return 'undated'
    localDT = utcToLocalTime(utcDT)
    now = datetime.datetime.now(pytz.utc)
    if localDT.toordinal() == now.toordinal():
        # if today, leave off date
        return 'Today %s' % localDT.strftime('%H:%M')
    elif localDT.toordinal() == now.toordinal() - 1:
        # if yesterday, express date as 'Yesterday'
        return 'Yesterday %s' % localDT.strftime('%H:%M')
    elif localDT.year == now.year:
        # if same year, express date as 'Tue Jan 01'
        return localDT.strftime('%a %b %d %H:%M')
    else:
        # if different year, express date as '2007 Jan 01'
        return localDT.strftime('%Y %b %d %H:%M')


def parse0(s):
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d-%H:%M')
    except ValueError:
        return None


def stringToLocalDT(s, intervalStart=True, now=None):
    """Converts @s to corresponding local datetime.  Legal string
    formats are .  If string specifies only high-order fields (year or
    year/month/day), return start or end of interval if @intervalStart
    is True or False, respectively.  If string specifies only low-order
    fields (month/day/time or time), fill in high-order fields with
    values from @now.  If @now is not specified, it defaults to the
    current time.'"""

    if now is None:
        now = datetime.datetime.now(pytz.utc)
    strftime = datetime.datetime.strftime
    bigDefaults = now
    if intervalStart:
        # 1901 is min valid value for strftime
        littleDefaults = datetime.datetime.min.replace(year=1901)
    else:
        littleDefaults = datetime.datetime.max

    # YYYY-mm-dd-HH:MM
    result = parse0(s)
    if result:
        return result

    # mm-dd-HH:MM
    full = '%s-%s' % (strftime(bigDefaults, '%Y'), s)
    result = parse0(full)
    if result:
        return result

    # HH:MM
    full = '%s-%s' % (strftime(bigDefaults, '%Y-%m-%d'), s)
    result = parse0(full)
    if result:
        return result

    # YYYY-mm-dd
    full = '%s-%s' % (s, strftime(littleDefaults, '%H:%M'))
    result = parse0(full)
    if result:
        return result

    # YYYY
    full = '%s-%s' % (s, strftime(littleDefaults, '%m-%d-%H:%M'))
    result = parse0(full)
    if result:
        return result

    raise ValueError("times must be formatted as YYYY-mm-dd-HH:MM, mm-dd-HH:MM, HH:MM, YYYY-mm-dd, or YYYY")


def stringToUtcDT(s, intervalStart=True, now=None):
    return localToUtcTime(stringToLocalDT(s, intervalStart, now))


def parseCsvTime(timeStr):
    '''Parse times GeoCam Share 2009 placed in export CSV files.  The
    same format was used in the upload form by GeoCam Mobile 2009'''
    # strip microseconds if present
    timeStr = re.sub(r'\.\d+$', '', timeStr)
    return datetime.datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S')


def parseUploadTime(timeStr):
    try:
        # format used by GeoCam Mobile 2009
        return parseCsvTime(timeStr)
    except ValueError:
        pass

    try:
        # ISO 8601 format we should probably use in the future
        return iso8601.parse_date(timeStr)
    except iso8601.ParseError:
        pass

    try:
        # POSIX time stamp may be easier to produce for some clients
        posixTimeStamp = float(timeStr)
    except ValueError:
        pass
    else:
        return datetime.datetime.fromtimestamp(posixTimeStamp)

    # hm, nothing worked
    raise ValueError('could not parse datetime from %s' % timeStr)


def getTimeShort(utcDt, tz=None, now=None):
    # tell pylint not to complain about too many branches and return statements
    # pylint: disable=R0911,R0912

    if now is None:
        now = datetime.datetime.now(pytz.utc)
    diff = now - utcDt
    diffSecs = diff.days * 24 * 60 * 60 + diff.seconds
    diffMins = diffSecs // 60

    if diffMins < 1:
        return 'seconds ago'
    elif diffMins < 2:
        return '1 minute ago'
    elif diffMins < 60:
        return '%s minutes ago' % diffMins
    else:
        diffHours = diffMins // 60
        if diffHours < 2:
            return '1 hour ago'
        elif diffHours < 24:
            return '%s hours ago' % diffHours
        else:
            # zero out times so difference in days is right
            utcDay = utcDt.replace(hour=0, minute=0, second=0, microsecond=0)
            nowDay = now.replace(hour=0, minute=0, second=0, microsecond=0)
            diffDays = (nowDay - utcDay).days
            if diffDays < 2:
                return 'Yesterday'
            elif diffDays < 5:
                return '%s days ago' % diffDays
            else:
                if tz:
                    localizedDt = pytz.utc.localize(utcDt).astimezone(tz)
                else:
                    localizedDt = utcDt
                if utcDt.year == now.year:
                    return localizedDt.strftime('%b %e')
                else:
                    return localizedDt.strftime('%Y-%m-%d')


def convert_time_with_zone(event_time, timezone):
    """
    Clean a time in a form
    :param event_time:
    :param timezone:
    :return: datetime aware time
    """
    if not event_time:
        return None
    else:
        if timezone:
            tz = pytz.timezone(timezone)
            if not event_time.tzinfo:
                event_time = tz.localize(event_time)
            elif event_time.tzinfo and event_time.tzinfo.zone != timezone:
                # it will come in as a datetime aware time
                event_time = event_time.replace(tzinfo=None)
                event_time = tz.localize(event_time)
        if event_time.tzinfo != pytz.utc:
            event_time = timeZoneToUtc(event_time)
        return event_time


def clean_timezone(incoming_timezone):
    if incoming_timezone== 'utc':
        return 'Etc/UTC'
    else:
        return incoming_timezone
    return None


def hms_to_total_s(hms_string):
    """
    Convert HH:mm:ss to total seconds
    :param hms_string: HH:mm:ss
    :return: total seconds
    """
    tokens = hms_string.split(':')
    if len(tokens) == 3:
        h = tokens[0]
        m = tokens[1]
        s = tokens[2]
    elif len(tokens) == 2:
        h = 0
        m = tokens[0]
        s = tokens[1]
    elif len(tokens) == 1:
        h = 0
        m = 0
        s = tokens[0]
    ans = int(s) + int(m) * 60 + int(h) * 60 * 60
    return ans


def seconds_to_minutes_seconds(seconds, zero_seconds_if_minutes=False):
    """
    Convert a seconds value which may be > 0 into minutes, seconds
    :param seconds: the seconds
    :param zero_seconds_if_minutes: True to zero out the seconds if minutes > 0
    :return: minutes, seconds
    """
    result_seconds = seconds
    result_minutes = 0
    if result_seconds >= 60:
        result_minutes = int(result_seconds / 60)
        if zero_seconds_if_minutes:
            result_seconds = 0
    return result_minutes, result_seconds