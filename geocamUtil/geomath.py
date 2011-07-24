
import math

EARTH_RADIUS_METERS = 6371010
DEG2RAD = math.pi / 180.0
RAD2DEG = 180.0 / math.pi

def calculateDiffMeters(a, b):
    """
    a and b are WGS84 lat/lon coordinates.  returns [x,y] displacement
    in meters that would get you from b to a.  x is easting and y is
    northing.
    """

    # this is a crude approximation but works fine locally, probably
    # within 1% for distances under 10 km and latitude within +/- 75
    # degrees.
    latDiff = (a[1] - b[1]) * DEG2RAD
    lonDiff = (a[0] - b[0]) * DEG2RAD
    lat = 0.5 * (a[1] + b[1]) * DEG2RAD
    return [math.cos(lat) * EARTH_RADIUS_METERS * lonDiff,
            EARTH_RADIUS_METERS * latDiff]

def addMeters(latLon, xy):
    """
    approximate inverse of calculateDiffMeters

    diff = calculateDiffMeters(a, b) <-> a = addMeters(b, diff)
    """

    x = xy[0]
    y = xy[1]
    latRad = latLon[1] * DEG2RAD
    latDiff = y / EARTH_RADIUS_METERS
    lonDiff = x / (math.cos(latRad) * EARTH_RADIUS_METERS)
    return [latLon[0] + RAD2DEG * lonDiff,
            latLon[1] + RAD2DEG * latDiff]

def xyFromPolar(rangeMeters, bearingDegrees):
    thetaRadians = DEG2RAD * (90.0 - bearingDegrees)
    x = rangeMeters * math.cos(thetaRadians)
    y = rangeMeters * math.sin(thetaRadians)
    return [x, y]

def getLength(v):
    x = v[0]
    y = v[1]
    return math.sqrt(x*x + y*y)

def getBearingDegrees(v):
    x = v[0]
    y = v[1]
    result = 90.0 - RAD2DEG * math.atan2(y, x)
    if result < 0:
        result += 360
    return result
