# __NO_RELICENSE__
# ***************************************************************************
# *  usng.js  (U.S. National Grid functions)
# *  Module to calculate National Grid Coordinates
# *
# *  last change or bug fix: February 2009
# *  [Translated to Python by GeoCam Project]
# ****************************************************************************/
#
# Copyright (c) 2009 Larry Moore, jane.larry@gmail.com
# Released under the MIT License; see
# http:#www.opensource.org/licenses/mit-license.php
# or http:#en.wikipedia.org/wiki/MIT_License
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
#*****************************************************************************
#
#    References and history of this code:
#
#    For detailed information on the U.S. National Grid coordinate system,
#    see  http:#www.fgdc.gov/usng
#
#    Reference ellipsoids derived from Peter H. Dana's website-
#    http:#www.utexas.edu/depts/grg/gcraft/notes/datum/elist.html
#    Department of Geography, University of Texas at Austin
#    Internet: pdana@mail.utexas.edu
#
#    Technical reference:
#    Defense Mapping Agency. 1987b. DMA Technical Report: Supplement to
#    Department of Defense World Geodetic System 1984 Technical Report. Part I
#    and II. Washington, DC: Defense Mapping Agency
#
#    Originally based on C code written by Chuck Gantz for UTM calculations
#    http:#www.gpsy.com/gpsinfo/geotoutm/     -- chuck.gantz@globalstar.com
#
#    Converted from C to JavaScript by Grant Wong for use in the
#    USGS National Map Project in August 2002
#
#    Modifications and developments continued by Doug Tallman from
#    December 2002 through 2004 for the USGS National Map viewer
#
#    Adopted with modifications by Larry Moore, January 2007,
#    for GoogleMaps application;
#    http:#www.fidnet.com/~jlmoore/usng
#
#    Assumes a datum of NAD83 (or its international equivalent WGS84).
#    If NAD27 is used, set IS_NAD83_DATUM to 'False'. (This does
#    not do a datum conversion; it only allows either datum to
#    be used for geographic-UTM/USNG calculations.)
#    NAD83 and WGS84 are equivalent for all practical purposes.
#    (NAD27 computations are irrelevant to Google Maps applications)
#
#
#*************************************************************************
# programmer interface summary
#
# 1) convert lat/lng decimal degrees to a USNG string
# function LLtoUSNG(lat, lon, precision)
#    inputs are in decimal degrees, west longitude negative, south latitude negative
#    'precision' specifies the number of digits in output coordinates
#         e.g. 5 specifies 1-meter precision (see USNG standard for explanation)
#         One digit:    10 km precision      eg. "18S UJ 2 1"
#         Two digits:   1 km precision       eg. "18S UJ 23 06"
#         Three digits: 100 meters precision eg. "18S UJ 234 064"
#         Four digits:  10 meters precision  eg. "18S UJ 2348 0647"
#         Five digits:  1 meter precision    eg. "18S UJ 23480 06470"
#    return value is a USNG coordinate as a text string
#    the return value contains spaces to improve readability, as permitted by
#        the USNG standard
#        the form is NNC CC NNNNN NNNNN
#        if a different format or precision is desired, the calling application
#            must make the changes
#
# 2) convert a USNG string to lat/lng decimal degrees
# function USNGtoLL(usng_string,latlng)
#    the following formats of the input string are supported:
#        NNCCCNNNNNNNNNN
#        NNC CC NNNNNNNNNN
#        NNC CC NNNNN NNNNN
#        all precisions of the easting and northing coordinate values are also supported
#             e.g. NNC CC NNN NNN
#    output is a 2-element array latlng declared by the calling routine
#        for example, calling routine contains the line var latlng=[]
#        latlng[0] contains latitude, latlng[1] contains longitude
#           both in decimal degrees, south negative, west negative
#
# 3) convert lat/lng decimal degrees to MGRS string (same as USNG string, but with
#    no space delimeters)
# function LLtoMGRS(lat, lon, precision)
#   create a string of Military Grid Reference System coordinates
#   Same as LLtoUSNG, except that output cannot contain space delimiters;
#   NOTE: this is not a full implementation of MGRS.  It won't deal with numbers
#         near the poles, but only in the UTM domain of 84N to 80S
#
# 4) wrapper for USNGtoLL to return an instance of GLatLng
# function GUsngtoLL(usngstr)
#   input is a USNG or MGRS string
#   return value is an instance of GLatLng
#   use this only with Google Maps applications; USNGtoLL is more generic
#
# 5) evaluates a string to see if it is a legal USNG coordinate; if so, returns
#       the string modified to be all upper-case, non-delimited; if not, returns 0
# function isUSNG(inputStr)
#
# for most purposes, these five function calls are the only things an application programmer
# needs to know to use this module.
#
# Note regarding UTM coordinates: UTM calculations are an intermediate step in lat/lng-USNG
# conversions, and can also be captured by applications, using functions below that are not
# summarized in the above list.
# The functions in this module use negative numbers for UTM Y values in the southern
# hemisphere.  The calling application must check for this, and convert to correct
# southern-hemisphere values by adding 10,000,000 meters.
#

import math
import re
import json

# suppress style complaint about functions with 'too many' return statements
# pylint: disable=R0911

# suppress bogus complaints about defining members outside of
# constructors and using unknown class members
# pylint: disable=W0201,E1101

############################################################################

ngFunctionsPresent = True
UNDEFINED_STR = "undefined"
# UTMEasting
# UTMNorthing
# UTMZone      # 3 chars...two digits and letter
# zoneNumber   # integer...two digits


################################# Constants ################################

FOURTHPI = math.pi / 4
DEG_2_RAD = math.pi / 180
RAD_2_DEG = 180.0 / math.pi
BLOCK_SIZE = 100000  # size of square identifier (within grid zone designation, meters)

IS_NAD83_DATUM = True  # if False, assumes NAD27 datum

# For diagram of zone sets, please see the "United States National Grid" white paper.
GRIDSQUARE_SET_COL_SIZE = 8  # column width of grid square set
GRIDSQUARE_SET_ROW_SIZE = 20  # row height of grid square set

# UTM offsets
EASTING_OFFSET = 500000.0  # (meters)
NORTHING_OFFSET = 10000000.0  # (meters)

# scale factor of central meridian
k0 = 0.9996

# check for NAD83
if IS_NAD83_DATUM:
    EQUATORIAL_RADIUS = 6378137.0  # GRS80 ellipsoid (meters)
    ECC_SQUARED = 0.006694380023

# else NAD27 datum is assumed
else:
    EQUATORIAL_RADIUS = 6378206.4  # Clarke 1866 ellipsoid (meters)
    ECC_SQUARED = 0.006768658

ECC_PRIME_SQUARED = ECC_SQUARED / (1 - ECC_SQUARED)

# variable used in inverse formulas (UTMtoLL function)
E1 = (1 - math.sqrt(1 - ECC_SQUARED)) / (1 + math.sqrt(1 - ECC_SQUARED))

# Number of digits to display for x,y coords
#  One digit:    10 km precision      eg. "18S UJ 2 1"
#  Two digits:   1 km precision       eg. "18S UJ 23 06"
#  Three digits: 100 meters precision eg. "18S UJ 234 064"
#  Four digits:  10 meters precision  eg. "18S UJ 2348 0647"
#  Five digits:  1 meter precision    eg. "18S UJ 23480 06470"


############## retrieve zone number from latitude, longitude #############
#
#    Zone number ranges from 1 - 60 over the range [-180 to +180]. Each
#    range is 6 degrees wide. Special cases for points outside normal
#    [-80 to +84] latitude zone.
#
########################################################################
def getZoneNumber(lat, lon):

    lat = float(lat)
    lon = float(lon)

    # sanity check on input
    #////////////////////////////////   /*
    #  if (lon > 360 || lon < -180 || lat > 90 || lat < -90) {
    #    alert('Bad input. lat: ' + lat + ' lon: ' + lon)
    #  }
    #////////////////////////////////  */

    # convert 0-360 to [-180 to 180] range
    lonTemp = (lon + 180) - int((lon + 180) / 360) * 360 - 180

    # Handle special case of west coast of Norway
    if lat >= 56.0 and lat < 64.0 and lonTemp >= 3.0 and lonTemp < 12.0:
        return 32

    # Special zones for Svalbard
    if (72.0 <= lat < 84.0):
        if (0.0 <= lonTemp < 9.0):
            return 31

        if (9.0 <= lonTemp < 21.0):
            return 33

        if (21.0 <= lonTemp < 33.0):
            return 35

        if (33.0 <= lonTemp < 42.0):
            return 37

    return int((lonTemp + 180) / 6) + 1


################# convert latitude, longitude to UTM  ###################
#
#    Converts lat/long to UTM coords.  Equations from USGS Bulletin 1532
#    (or USGS Professional Paper 1395 "Map Projections - A Working Manual",
#    by John P. Snyder, U.S. Government Printing Office, 1987.)
#
#   East Longitudes are positive, West longitudes are negative.
#    North latitudes are positive, South latitudes are negative
#    lat and lon are in decimal degrees
#
#    output is in the input array utmcoords
#        utmcoords[0] = easting
#        utmcoords[1] = northing (NEGATIVE value in southern hemisphere)
#        utmcoords[2] = zone
#
###########################################################################
def LLtoUTM(lat, lon, zoneNumber=None, zoneLetter=None):
    # utmcoords is a 2-D array declared by the calling routine

    lat = float(lat)
    lon = float(lon)

    # Constrain reporting USNG coords to the latitude range [80S .. 84N]
    ########
    if not (-80.0 < lat < 84.0):
        return UNDEFINED_STR
    ###########

    # sanity check on input - turned off when testing with Generic Viewer
    ##########/  /*
    if not ((-180 < lon < 360) and (-90 < lat < 90)):
        raise ValueError('Bad input. lat: ' + lat + ' lon: ' + lon)
    ###########  */

    # Make sure the longitude is between -180.00 .. 179.99..
    # Convert values on 0-360 range to this range.
    lonTemp = (lon + 180) - int((lon + 180) / 360) * 360 - 180
    latRad = lat * DEG_2_RAD
    lonRad = lonTemp * DEG_2_RAD

    # user-supplied zone number will force coordinates to be computed in a particular zone
    if zoneNumber == None:
        zoneNumber = getZoneNumber(lat, lon)
    if zoneLetter == None:
        zoneLetter = UTMLetterDesignator(lat)

    lonOrigin = (zoneNumber - 1) * 6 - 180 + 3  # +3 puts origin in middle of zone
    lonOriginRad = lonOrigin * DEG_2_RAD

    # compute the UTM Zone from the latitude and longitude
    _UTMZone = str(zoneNumber) + UTMLetterDesignator(lat) + " "

    N = EQUATORIAL_RADIUS / math.sqrt(1 - ECC_SQUARED *
                                      math.sin(latRad) * math.sin(latRad))
    T = math.tan(latRad) * math.tan(latRad)
    C = ECC_PRIME_SQUARED * math.cos(latRad) * math.cos(latRad)
    A = math.cos(latRad) * (lonRad - lonOriginRad)

    # Note that the term Mo drops out of the "M" equation, because phi
    # (latitude crossing the central meridian, lambda0, at the origin of the
    #  x,y coordinates), is equal to zero for UTM.
    M = (EQUATORIAL_RADIUS
         * ((1 - ECC_SQUARED / 4
              - 3 * (ECC_SQUARED * ECC_SQUARED) / 64
              - 5 * (ECC_SQUARED * ECC_SQUARED * ECC_SQUARED) / 256) * latRad
            - (3 * ECC_SQUARED / 8 + 3 * ECC_SQUARED * ECC_SQUARED / 32
                + 45 * ECC_SQUARED * ECC_SQUARED * ECC_SQUARED / 1024)
            * math.sin(2 * latRad) + (15 * ECC_SQUARED * ECC_SQUARED / 256
                                      + 45 * ECC_SQUARED * ECC_SQUARED * ECC_SQUARED / 1024) * math.sin(4 * latRad)
            - (35 * ECC_SQUARED * ECC_SQUARED * ECC_SQUARED / 3072) * math.sin(6 * latRad)))

    UTMEasting = (k0 * N
                  * (A + (1 - T + C) * (A * A * A) / 6
                     + (5 - 18 * T + T * T + 72 * C - 58 * ECC_PRIME_SQUARED)
                     * (A * A * A * A * A) / 120)
                  + EASTING_OFFSET)

    UTMNorthing = (k0 * (M + N * math.tan(latRad)
                         * ((A * A) / 2
                            + (5 - T + 9
                               * C + 4 * C * C) * (A * A * A * A) / 24
                            + (61 - 58 * T + T * T + 600 * C - 330 * ECC_PRIME_SQUARED)
                            * (A * A * A * A * A * A) / 720)))

    # added by LRM 2/08...not entirely sure this doesn't just move a bug somewhere else
    # utm values in southern hemisphere
    if UTMNorthing < 0:
        UTMNorthing += NORTHING_OFFSET

    return (UTMEasting, UTMNorthing, zoneNumber, zoneLetter)

# end LLtoUTM


################# convert latitude, longitude to USNG  ###################
#   Converts lat/lng to USNG coordinates.  Calls LLtoUTM first, then
#   converts UTM coordinates to a USNG string.
#
#    Returns string of the format: DDL LL DDDD DDDD (4-digit precision), eg:
#      "18S UJ 2286 0705" locates Washington Monument in Washington, D.C.
#      to a 10-meter precision.
#
###########################################################################

def UTMtoUSNG(utmEasting, utmNorthing, utmZoneNumber, utmLatBand, precision):
    usngLetters = findGridLetters(utmZoneNumber, utmNorthing, utmEasting)
    usngNorthing = int(round(utmNorthing)) % BLOCK_SIZE
    usngEasting = int(round(utmEasting)) % BLOCK_SIZE

    # added... truncate digits to achieve specified precision
    usngNorthing = int(math.floor(usngNorthing / math.pow(10, (5 - precision))))
    usngEasting = int(math.floor(usngEasting / math.pow(10, (5 - precision))))
    usng = str(utmZoneNumber) + utmLatBand + " " + usngLetters + " "

    # REVISIT: Modify to incorporate dynamic precision ?
    for _i in xrange(len(str(usngEasting)), precision):
        usng += "0"
    usng += str(usngEasting) + " "

    for _i in xrange(len(str(usngNorthing)), precision):
        usng += "0"
    usng += str(usngNorthing)

    return usng


def LLtoUSNG(lat, lon, precision):
    lat = float(lat)
    lon = float(lon)

    # convert lat/lon to UTM coordinates
    UTMEasting, UTMNorthing, zoneNumber, zoneLetter = LLtoUTM(lat, lon)

    return UTMtoUSNG(UTMEasting, UTMNorthing, zoneNumber, zoneLetter, precision)


############### retrieve grid zone designator letter ######################
#
#    This routine determines the correct UTM letter designator for the given
#    latitude returns 'Z' if latitude is outside the UTM limits of 84N to 80S
#
#    Returns letter designator for a given latitude.
#    Letters range from C (-80 lat) to X (+84 lat), with each zone spanning
#    8 degrees of latitude.
#
###########################################################################

def UTMLetterDesignator(lat):
    lat = float(lat)

    if ((84 >= lat) and (lat >= 72)):
        return 'X'
    if ((72 > lat) and (lat >= 64)):
        return 'W'
    if ((64 > lat) and (lat >= 56)):
        return 'V'
    if ((56 > lat) and (lat >= 48)):
        return 'U'
    if ((48 > lat) and (lat >= 40)):
        return 'T'
    if ((40 > lat) and (lat >= 32)):
        return 'S'
    if ((32 > lat) and (lat >= 24)):
        return 'R'
    if ((24 > lat) and (lat >= 16)):
        return 'Q'
    if ((16 > lat) and (lat >= 8)):
        return 'P'
    if 0 <= lat < 8:
        return 'N'
    if -8 <= lat < 0:
        return 'M'
    if -16 <= lat < -8:
        return 'L'
    if -24 <= lat < -16:
        return 'K'
    if -32 <= lat < -24:
        return 'J'
    if -40 <= lat < -32:
        return 'H'
    if -48 <= lat < -40:
        return 'G'
    if -56 <= lat < -48:
        return 'F'
    if -64 <= lat < -56:
        return 'E'
    if -72 <= lat < -64:
        return 'D'
    if -80 <= lat < -72:
        return 'C'
    # This is here as an error flag to show
    # that the latitude is outside the UTM limits
    return 'Z'


################## Find the set for a given zone. ########################
#
#    There are six unique sets, corresponding to individual grid numbers in
#    sets 1-6, 7-12, 13-18, etc. Set 1 is the same as sets 7, 13, ..; Set 2
#    is the same as sets 8, 14, ..
#
#    See p. 10 of the "United States National Grid" white paper.
#
###########################################################################

def findSet(zoneNum):
    zoneNum = int(zoneNum)
    zoneNum = zoneNum % 6
    if zoneNum == 0:
        return 6
    if zoneNum <= 5:
        return zoneNum
    return -1


###########################################################################
#  Retrieve the square identification for a given coordinate pair & zone
#  See "lettersHelper" function documentation for more details.
#
###########################################################################

def findGridLetters(zoneNum, northing, easting):
    zoneNum = int(zoneNum)
    northing = float(northing)
    easting = float(easting)
    row = 1

    # northing coordinate to single-meter precision
    north_1m = int(round(northing))

    # Get the row position for the square identifier that contains the point
    while north_1m >= BLOCK_SIZE:
        north_1m = north_1m - BLOCK_SIZE
        row += 1

    # cycle repeats (wraps) after 20 rows
    row = row % GRIDSQUARE_SET_ROW_SIZE
    col = 0

    # easting coordinate to single-meter precision
    east_1m = int(round(easting))

    # Get the column position for the square identifier that contains the point
    while east_1m >= BLOCK_SIZE:
        east_1m = east_1m - BLOCK_SIZE
        col += 1

    # cycle repeats (wraps) after 8 columns
    col = col % GRIDSQUARE_SET_COL_SIZE

    return lettersHelper(findSet(zoneNum), row, col)


###########################################################################
#    Retrieve the Square Identification (two-character letter code), for the
#    given row, column and set identifier (set refers to the zone set:
#    zones 1-6 have a unique set of square identifiers; these identifiers are
#    repeated for zones 7-12, etc.)
#
#    See p. 10 of the "United States National Grid" white paper for a diagram
#    of the zone sets.
#
###########################################################################
def lettersHelper(lset, row, col):
    # handle case of last row
    if row == 0:
        row = GRIDSQUARE_SET_ROW_SIZE - 1
    else:
        row -= 1

    # handle case of last column
    if col == 0:
        col = GRIDSQUARE_SET_COL_SIZE - 1
    else:
        col -= 1

    if lset == 1:
        l1 = "ABCDEFGH"
        l2 = "ABCDEFGHJKLMNPQRSTUV"
        return l1[col] + l2[row]

    if lset == 2:
        l1 = "JKLMNPQR"
        l2 = "FGHJKLMNPQRSTUVABCDE"
        return l1[col] + l2[row]

    if lset == 3:
        l1 = "STUVWXYZ"
        l2 = "ABCDEFGHJKLMNPQRSTUV"
        return l1[col] + l2[row]

    if lset == 4:
        l1 = "ABCDEFGH"
        l2 = "FGHJKLMNPQRSTUVABCDE"
        return l1[col] + l2[row]

    if lset == 5:
        l1 = "JKLMNPQR"
        l2 = "ABCDEFGHJKLMNPQRSTUV"
        return l1[col] + l2[row]

    if lset == 6:
        l1 = "STUVWXYZ"
        l2 = "FGHJKLMNPQRSTUVABCDE"
    return l1[col] + l2[row]


# Equations from USGS Bulletin 1532
# Written by Chuck Gantz- chuck.gantz@globalstar.com
def UTMtoLL(east, north, zoneNumber, zoneLetter):
    a = EQUATORIAL_RADIUS
    e2 = ECC_SQUARED
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))

    x = east - 500000.0  # remove 500,000 meter offset for longitude
    if zoneLetter < 'N':
        hemiNumber = 1
    else:
        hemiNumber = 0
    y = north - hemiNumber * 1e+7

    lonOrigin = (zoneNumber - 1) * 6 - 180 + 3  # +3 puts origin in middle of zone

    eccPrimeSquared = (e2) / (1 - e2)

    M = y / k0
    mu = M / (a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))

    phi1Rad = (mu + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * math.sin(2 * mu)
               + (21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * math.sin(4 * mu)
               + (151 * e1 * e1 * e1 / 96) * math.sin(6 * mu))
    _phi1 = phi1Rad * RAD_2_DEG

    N1 = a / math.sqrt(1 - e2 * math.sin(phi1Rad) * math.sin(phi1Rad))
    T1 = math.tan(phi1Rad) * math.tan(phi1Rad)
    C1 = eccPrimeSquared * math.cos(phi1Rad) * math.cos(phi1Rad)
    R1 = a * (1 - e2) / pow(1 - e2 * math.sin(phi1Rad) * math.sin(phi1Rad), 1.5)
    D = x / (N1 * k0)

    lat = (phi1Rad - (N1 * math.tan(phi1Rad) / R1)
           * (D * D / 2 - (5 + 3 * T1 + 10 * C1 - 4 * C1 * C1 - 9 * eccPrimeSquared) * D * D * D * D / 24
              + (61 + 90 * T1 + 298 * C1 + 45 * T1 * T1 - 252 * eccPrimeSquared - 3 * C1 * C1) * D * D * D * D * D * D / 720))
    dlon = ((D - (1 + 2 * T1 + C1) * D * D * D / 6 + (5 - 2 * C1 + 28 * T1 - 3 * C1 * C1 + 8 * eccPrimeSquared + 24 * T1 * T1)
              * D * D * D * D * D / 120) / math.cos(phi1Rad))
    return (RAD_2_DEG * lat, lonOrigin + RAD_2_DEG * dlon)


class Struct(object):
    def __repr__(self):
        return json.dumps(vars(self), indent=4)

####################### USNG to UTM ######################################
#
#    The Following functions are used to convert USNG Cords to UTM Cords.
#
###########################################################################
UTMGzdLetters = "NPQRSTUVWX"
USNGSqEast = "ABCDEFGHJKLMNPQRSTUVWXYZ"
USNGSqLetOdd = "ABCDEFGHJKLMNPQRSTUV"
USNGSqLetEven = "FGHJKLMNPQRSTUVABCDE"
###################################################################################
#
#                   USNGtoUTM(zone,let,sq1,sq2,east,north,ret)
#Expected Input args:
#      zone: Zone (integer), eg. 18
#      let: Zone letter, eg S
#      sq1:  1st USNG square letter, eg U
#      sq2:  2nd USNG square Letter, eg J
#      east:  Easting digit string, eg 4000
#      north:  Northing digit string eg 4000
#      ret:  saves zone,let,Easting and Northing as properties ret
#
###################################################################################

GZD_LETTERS = "CDEFGHJKLMNPQRSTUVWX"
USNG_LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"


def USNGtoUTM(zone, let, sq1, sq2, east, north):
    # see FGDC-STD-011-2001 page 10
    colLetter = sq1
    colSet = ((zone - 1) % 3)
    colIndex0 = USNG_LETTERS.find(colLetter)
    colIndex = colIndex0 + 1 - GRIDSQUARE_SET_COL_SIZE * colSet

    rowLetter = sq2
    rowSet = ((zone - 1) % 2)
    rowIndex0 = USNG_LETTERS.find(rowLetter)
    rowIndex1 = rowIndex0 - 5 * rowSet

    latBandLetter = let
    latBandRowIndex = latBandMidpointRowIndex(latBandLetter)

    # choose numCycles such that rowIndex is as close as possible to
    # latBandRowIndex.  because a set of 20 rows is much taller than a
    # latitude band, the rounding operation should never be a "close
    # call".
    numCycles = int(round((latBandRowIndex - rowIndex0) / GRIDSQUARE_SET_ROW_SIZE))
    rowIndex = numCycles * GRIDSQUARE_SET_ROW_SIZE + rowIndex1

    ret = Struct()
    ret.N = rowIndex * BLOCK_SIZE + float(north) * math.pow(10, 5 - len(north))
    ret.E = colIndex * BLOCK_SIZE + float(east) * math.pow(10, 5 - len(east))
    ret.zone = zone
    ret.letter = let
    return ret


def USNGtoUTMold(zone, let, sq1, sq2, east, north):
    # Starts (southern edge) of N-S zones in millons of meters
    zoneBase = [1.1, 2.0, 2.9, 3.8, 4.7, 5.6, 6.5, 7.3, 8.2, 9.1,
                0, 0.8, 1.7, 2.6, 3.5, 4.4, 5.3, 6.2, 7.0, 7.9]

    # Starts of 2 million meter segments, indexed by zone
    segBase = [0, 2, 2, 2, 4, 4, 6, 6, 8, 8,
               0, 0, 0, 2, 2, 4, 4, 6, 6, 6]

    # convert easting to UTM
    eSqrs = USNGSqEast.find(sq1)
    appxEast = 1 + eSqrs % 8

    # convert northing to UTM
    letNorth = "CDEFGHJKLMNPQRSTUVWX".find(let)
    if zone % 2 != 0:  # odd number zone
        nSqrs = "ABCDEFGHJKLMNPQRSTUV".find(sq2)
    else:  # even number zone
        nSqrs = "FGHJKLMNPQRSTUVABCDE".find(sq2)

    zoneStart = zoneBase[letNorth]
    appxNorth = float(segBase[letNorth]) + nSqrs / 10
    if appxNorth < zoneStart:
        appxNorth += 2

    ret = Struct()
    ret.N = appxNorth * 1000000 + float(north) * math.pow(10, 5 - len(north))
    ret.E = appxEast * 100000 + float(east) * math.pow(10, 5 - len(east))
    ret.zone = zone
    ret.letter = let
    return ret


# parse a USNG string and feed results to USNGtoUTM, then the results of that to UTMtoLL
def USNGtoLL(usngStr_input):
    usngp = Struct()

    parseUSNG_str(usngStr_input, usngp)
    coords = Struct()

    # convert USNG coords to UTM; this routine counts digits and sets precision
    coords = USNGtoUTM(usngp.zone, usngp.let, usngp.sq1, usngp.sq2, usngp.east, usngp.north)

    return UTMtoLL(coords.E, coords.N, usngp.zone, usngp.let)


def latBandMidpointLatitude(latBandLetter):
    if latBandLetter == 'X':
        # the northernmost band X is 12 degrees wide, special case
        return 78
    else:
        # southernmost band C has midpoint at 76 South, 8 degrees per band
        gzdIndex = GZD_LETTERS.find(latBandLetter)
        return -76 + gzdIndex * 8


def latBandMidpointRowIndex(latBandLetter):
    lat = latBandMidpointLatitude(latBandLetter)
    _easting, northing, _zoneNumber, _zoneLetter = LLtoUTM(lat, 0)
    return northing / BLOCK_SIZE


# convert lower-case characters to upper case, remove space delimeters, separate string into parts
def parseUSNG_str(usngStr_input, parts):
    usngStr_temp = usngStr_input.upper()

    # put usgn string in 'standard' form with no space delimiters
    usngStr = re.sub(r'%20', "", usngStr_temp)
    usngStr = re.sub(r' ', "", usngStr_temp)

    if len(usngStr) < 7:
        raise ValueError("This application requires minimum USNG precision of 10,000 meters")

    # break usng string into its component pieces
    parts.zone = int(usngStr[0]) * 10 + int(usngStr[1]) * 1
    parts.let = usngStr[2]
    parts.sq1 = usngStr[3]
    parts.sq2 = usngStr[4]
    # parts.zone = usngStr.charAt(j++)*10 + usngStr.charAt(j++)*1
    # parts.let = usngStr.charAt(j++)
    # parts.sq1 = usngStr.charAt(j++)
    # parts.sq2 = usngStr.charAt(j++)

    parts.precision = (len(usngStr) - 5) / 2
    #parts.precision = (len(usngStr)-j) / 2
    parts.east = usngStr[5:(5 + parts.precision)]
    parts.north = usngStr[(5 + parts.precision):]


# checks a string to see if it is valid USNG
#    if so, returns the string in all upper case, no delimeters
#    if not, returns 0
def isUSNG(inputStr):
    # convert all letters to upper case
    usngStr = inputStr.upper()

    # put usng string in 'standard' form with no space delimiters
    usngStr = re.sub(r'%20', "", usngStr)
    usngStr = re.sub(r' ', "", usngStr)

    if len(usngStr) > 15:
        return 0

    strregexp = r"^[0-9]{2}[CDEFGHJKLMNPQRSTUVWX]$"
    if re.match(strregexp, usngStr):
        print "Input appears to be a UTM zone...more precision is required to display a correct result."
        return 0

    strregexp = r"^[0-9]{2}[CDEFGHJKLMNPQRSTUVWX][ABCDEFGHJKLMNPQRSTUVWXYZ][ABCDEFGHJKLMNPQRSTUV]([0-9][0-9]){0,5}"
    if not re.match(strregexp, usngStr):
        return 0

    if len(usngStr) < 7:
        print usngStr, " Appears to be a USNG string, but this application requires precision of at least 10,000 meters"
        return 0

    # all tests passed...return the upper-case, non-delimited string
    return usngStr


# create a Military Grid Reference System string.  this is the same as a USNG string, but
#    with no spaces.  space delimiters are optional but allowed in USNG, but are not allowed
#    in MGRS notation.  but the numbers are the same.
def LLtoMGRS(lat, lon, precision):
    mgrs_str = ""
    usng_str = LLtoUSNG(lat, lon, precision)

    # remove space delimiters to conform to mgrs spec
    mgrs_str = re.sub(r' ', '', usng_str)

    return mgrs_str

# def LLtoUSNG_nad27(lat, lon, precision):
#     # set ellipsoid to Clarke 1866 (meters)
#     EQUATORIAL_RADIUS = 6378206.4
#     ECC_SQUARED = 0.006768658
#
#     usngstr = LLtoUSNG(lat, lon, precision)
#
#     # reset GRS80 ellipsoid
#     EQUATORIAL_RADIUS    = 6378137.0
#     ECC_SQUARED = 0.006694380023
#
#     return usngstr + " (NAD27)"
