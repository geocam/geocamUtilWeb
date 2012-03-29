#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import re
import json
import math
import tempfile
import os
import urllib
import sys

import usng

# colors expressed in KML's ABGR hex format
COLORS = {
    'white': 'ffffffff',
    'red': 'ff0000ff',
    'orange': 'ff0088ff',
    'cyan': 'ffffff00',
    'magenta': 'ffff00ff',
    'yellow': 'ff00ffff',
    'pale_cyan': 'ffffff99',
    'pale_yellow': 'ff99ffff',
    'pale_magenta': 'ffff99ff',
    'invisible': '00000000',
    }

ZONE_STYLE = {'color': 'red', 'width': 4}

GRIDS = (
    (500000, {'color': 'pale_yellow', 'width': 1}),
    (100000, {'color': 'pale_magenta', 'width': 1}),
    (50000, {'color': 'pale_magenta', 'width': 1}),
    (10000, {'color': 'pale_cyan', 'width': 1}),
    (5000, {'color': 'pale_cyan', 'width': 1}),
    (1000, {'color': 'pale_yellow', 'width': 1}),
    (500, {'color': 'pale_yellow', 'width': 1}),
    (100, {'color': 'pale_magenta', 'width': 1}),
    (50, {'color': 'pale_magenta', 'width': 1}),
    (10, {'color': 'pale_cyan', 'width': 1}),
    )

outDirG = None


def wrapKml(text):
    return ("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
%s
</kml>
""" % text)


def wrapFolder(kmlText):
    return '<Folder>%s</Folder>' % kmlText


def writeFile(fname, text):
    fdir = os.path.dirname(fname)
    if not os.path.exists(fdir):
        os.makedirs(fdir)
    file(fname, 'w').write(text)


def getKmlField(field, kmlText):
    return float(re.search(r'<%s>(.*)</%s>' % (field, field), kmlText).group(1))


def getUllrFromKml(kmlName):
    kmlText = file(kmlName, 'r').read()
    north = getKmlField('north', kmlText)
    south = getKmlField('south', kmlText)
    east = getKmlField('east', kmlText)
    west = getKmlField('west', kmlText)
    return (north, west, south, east)


def getLineString(s, t, color='white', width=1):
    if color != 'white' or width != 1:
        style = ("""
  <Style>
    <LineStyle>
      <color>%s</color>
      <width>%s</width>
    </LineStyle>
  </Style>
""" % (COLORS[color], width))
    else:
        style = ''
    return ("""
<Placemark>
  %(style)s
  <LineString>
    <tessellate>1</tessellate>
    <altitudeMode>clampToGround</altitudeMode>
    <coordinates>
%(slon).6f,%(slat).6f,0
%(tlon).6f,%(tlat).6f,0
    </coordinates>
  </LineString>
</Placemark>
""" % dict(style=style, slat=s[0], slon=s[1], tlat=t[0], tlon=t[1]))


def determinant(v0, v1):
    return (v0[0] * v1[1]) - (v0[1] * v1[0])


def vectorDiff(v0, v1):
    assert len(v0) == len(v1)
    return [v0[i] - v1[i] for i in xrange(len(v0))]


def lineIntersect(a, b):
    x1, y1 = a.s
    x2, y2 = a.t
    x3, y3 = b.s
    x4, y4 = b.t
    det12 = x1 * y2 - y1 * x2
    det34 = x3 * y4 - y3 * x4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    xi = (det12 * (x3 - x4) - (x1 - x2) * det34) / denom
    yi = (det12 * (y3 - y4) - (y1 - y2) * det34) / denom
    return (xi, yi)


class LineSegment(object):
    def __init__(self, s, t, zone=None, latBand=None):
        self.s = s
        self.t = t
        self.zone = zone
        self.latBand = latBand
        self.visible = True

    def __repr__(self):
        return json.dumps(vars(self), indent=4)

    def inBounds(self, pt):
        return (determinant(vectorDiff(self.t, self.s),
                            vectorDiff(pt, self.s))
                > 0)

    def blockMightBeInBounds(self, sw, ne):
        if self.inBounds(sw) or self.inBounds(ne):
            return True
        west, south = sw
        east, north = ne
        return self.inBounds([west, north]) or self.inBounds([east, south])

    def clip(self, bound):
        if bound.inBounds(self.s):
            if bound.inBounds(self.t):
                # both in bounds, nothing to do
                pass
            else:
                # only t out of bounds; move t to intersection with bound
                self.t = lineIntersect(self, bound)
        else:
            # s out of bounds
            if bound.inBounds(self.t):
                # only s out of bounds; move s to intersection with bound
                self.s = lineIntersect(self, bound)
            else:
                # both out of bounds
                self.visible = False

    def getPlacemark(self, **kwargs):
        if not self.visible:
            return ''
        slatlon = usng.UTMtoLL(self.s[0], self.s[1], self.zone, self.latBand)
        tlatlon = usng.UTMtoLL(self.t[0], self.t[1], self.zone, self.latBand)
        return getLineString(slatlon, tlatlon, **kwargs)


def getGridLine(srcUtm, dstUtm, clipLines):
    slat, slon = usng.UTMtoLL(*srcUtm)
    tlat, tlon = usng.UTMtoLL(*dstUtm)
    return ("""
<Placemark>
  <LineString>
    <tessellate>1</tessellate>
    <altitudeMode>clampToGround</altitudeMode>
    <coordinates>
%(slon).6f,%(slat).6f,0
%(tlon).6f,%(tlat).6f,0
    </coordinates>
  </LineString>
</Placemark>
""" % dict(slat=slat, slon=slon, tlat=tlat, tlon=tlon))


def degMinString(val):
    val = abs(val)
    degrees = int(val)
    minutes = 60.0 * (val - degrees)
    return u'%d&deg; %.4f\'' % (degrees, minutes)


def degMinSecString(val):
    val = abs(val)
    degrees = int(val)
    minutesFloat = 60.0 * (val - degrees)
    minutes = int(minutesFloat)
    seconds = 60.0 * (minutesFloat - minutes)
    return u'%d&deg; %d\' %.2f"' % (degrees, minutes, seconds)


def makeGridLinesBlock(opts, parentFile, utmZone, utmLatBand, bounds, i, j, x0, y0, resIndex, skipEdges=False):
    #print 'makeGridLinesBlock %s %s %s %s %s %s' % (utmZone, utmLatBand, bounds, x0, y0, resIndex)
    blockSize = GRIDS[resIndex][0]
    res, style = GRIDS[resIndex + 1]
    n = int(blockSize / res + 1e-5)
    #print '%s %s' % (res, n)

    xmax = x0 + n * res
    ymax = y0 + n * res

    for bound in bounds:
        if not bound.blockMightBeInBounds([x0, y0], [xmax, ymax]):
            if opts.verbose:
                print >> sys.stderr, 'out of bounds 1:'
                print >> sys.stderr, '   bound %s..%s %s..%s' % (bound.s[0], bound.t[0], bound.s[1], bound.t[1])
                print >> sys.stderr, '   block %s..%s %s..%s' % (x0, xmax, y0, ymax)
            return ''

    content = ''
    for k in xrange(0, n + 1):
        if skipEdges and k in (0, n):
            continue
        x = x0 + k * res
        seg = LineSegment([x, y0], [x, ymax], utmZone, utmLatBand)
        for bound in bounds:
            seg.clip(bound)
        content += seg.getPlacemark(**style)

    for k in xrange(0, n + 1):
        if skipEdges and k in (0, n):
            continue
        y = y0 + k * res
        seg = LineSegment([x0, y], [xmax, y], utmZone, utmLatBand)
        for bound in bounds:
            seg.clip(bound)
        content += seg.getPlacemark(**style)

    thisFile = os.path.join(os.path.dirname(parentFile), '%s_%s' % (i, j), 'a.kml')

    for ii in xrange(0, n):
        x = x0 + ii * res
        for jj in xrange(0, n):
            y = y0 + jj * res

            addMarker = not (skipEdges and ii == 0 and jj == 0)
            for bound in bounds:
                if not bound.inBounds([x, y]):
                    addMarker = False

            if addMarker:
                lat, lon = usng.UTMtoLL(x, y, utmZone, utmLatBand)
                precision = 5 - int(math.floor(math.log10(res)))
                usngCoords = usng.UTMtoUSNG(x, y, utmZone, utmLatBand, precision)
                latDir = 'N' if lat >= 0 else 'S'
                lonDir = 'E' if lon >= 0 else 'W'
                description = ('USNG: %s<br/>\n' % usngCoords
                               + 'Lat/lon:<br/>\n'
                               + '%.6f, %.6f<br/>\n' % (lat, lon)
                               + '%s %s, %s %s<br/>\n' % (degMinString(lat), latDir, degMinString(lon), lonDir)
                               + '%s %s, %s %s<br/>\n' % (degMinSecString(lat), latDir, degMinSecString(lon), lonDir))
                description = urllib.quote(description)
                icon = os.path.relpath(os.path.join(outDirG, 'corner.png'),
                                       os.path.dirname(thisFile))
                content += ("""
<Placemark>
  <Point>
    <coordinates>%(lon).6f,%(lat).6f</coordinates>
  </Point>
  <Style>
    <IconStyle>
      <Icon>
        <href>%(icon)s</href>
      </Icon>
      <heading>0</heading>
      <scale>0.3</scale>
      <hotSpot x="0.0" y="0.0" xunits="fraction" yunits="fraction"/>
    </IconStyle>
  </Style>
  <description><![CDATA[%(description)s]]></description>
</Placemark>
"""
                            % dict(lat=lat, lon=lon, icon=icon, description=description))
            if (resIndex + 2) < len(GRIDS):
                # recurse
                content += makeGridLinesBlock(opts, thisFile, utmZone, utmLatBand, bounds,
                                              ii, jj, x, y, resIndex + 1, skipEdges=True)

    region = getRegion([x0, y0], [xmax, ymax], utmZone, utmLatBand)

    return makeNetworkLink(parentFile, thisFile, content, region)


def makeNetworkLink(parentFile, childFile, text, region=''):
    text = re.sub(r'>\s+<', '><', text)
    text = urllib.unquote(text)
    if not text:
        return ''
    writeFile(childFile, wrapKml(wrapFolder(text)))
    name = os.path.basename(os.path.dirname(childFile))
    relPath = os.path.relpath(childFile, os.path.dirname(parentFile))
    return ("""
<NetworkLink>
  %(region)s
  <Link>
    <href>%(relPath)s</href>
  </Link>
</NetworkLink>
""" % dict(name=name, region=region, relPath=relPath))


def getRegion(utmSW, utmNE, utmZone, utmLatBand):
    south, west = usng.UTMtoLL(utmSW[0], utmSW[1], utmZone, utmLatBand)
    north, east = usng.UTMtoLL(utmNE[0], utmNE[1], utmZone, utmLatBand)
    return ("""
<Region>
  <LatLonAltBox>
    <north>%(north).6f</north>
    <south>%(south).6f</south>
    <east>%(east).6f</east>
    <west>%(west).6f</west>
  </LatLonAltBox>
  <Lod>
    <minLodPixels>384</minLodPixels>
  </Lod>
</Region>
""" % dict(north=north, south=south, east=east, west=west))


def makeGridLinesForZone(opts, parentFile, ullr, utmZone, isNorth):
    if opts.verbose:
        print >> sys.stderr, 'zone=%s isNorth=%s' % (utmZone, isNorth)

    north, west, south, east = ullr

    utmLatBand = usng.LLtoUTM(north, east, utmZone)[3]

    utmNE = usng.LLtoUTM(north, east, utmZone)[:2]
    utmNW = usng.LLtoUTM(north, west, utmZone)[:2]
    utmSW = usng.LLtoUTM(south, west, utmZone)[:2]
    utmSE = usng.LLtoUTM(south, east, utmZone)[:2]

    if opts.verbose:
        print >> sys.stderr, 'utmNE=%s\nutmNW=%s\nutmSW=%s\nutmSE=%s' % (utmNE, utmNW, utmSW, utmSE)

    bounds = []

    # add bounds for user request
    bounds.append(LineSegment(utmNE, utmNW))
    bounds.append(LineSegment(utmNW, utmSW))
    bounds.append(LineSegment(utmSW, utmSE))
    bounds.append(LineSegment(utmSE, utmNE))

    # add bounds for utm zone
    wzLon = -180 + 6 * (utmZone - 1)
    bounds.append(LineSegment(usng.LLtoUTM(north, wzLon, utmZone)[:2],
                              usng.LLtoUTM(south, wzLon, utmZone)[:2]))
    ezLon = wzLon + 6
    bounds.append(LineSegment(usng.LLtoUTM(south, ezLon, utmZone)[:2],
                              usng.LLtoUTM(north, ezLon, utmZone)[:2]))

    # add bounds for hemisphere
    eqWest = usng.LLtoUTM(0, west, utmZone)[:2]
    eqEast = usng.LLtoUTM(0, east, utmZone)[:2]
    if isNorth:
        bounds.append(LineSegment(eqWest, eqEast))
    else:
        # FIX this doesn't work for some reason for lake lander area
        pass  # bounds.append(LineSegment(eqEast, eqWest))

    utmWest = min(utmSW[0], utmNW[0])
    utmSouth = min(utmSW[1], utmSE[1])
    utmEast = max(utmNE[0], utmSE[0])
    utmNorth = max(utmNE[1], utmNW[1])

    if isNorth:
        hemi = 'north'
    else:
        hemi = 'south'
    thisFile = os.path.join(os.path.dirname(parentFile),
                            '%s%s' % (utmZone, hemi),
                            'a.kml')
    if opts.verbose:
        print >> sys.stderr, 'thisFile:', thisFile

    # iterate through all the top-level blocks for this zone/hemisphere
    userBlockSize = max(utmEast - utmWest, utmNorth - utmSouth)
    #print 'userBlockSize:', userBlockSize
    for i in xrange(1, len(GRIDS)):
        if GRIDS[i][0] * 2 <= userBlockSize:
            maxSizeIndex = i - 1
            break
    #print 'maxSizeIndex:', maxSizeIndex, GRIDS[maxSizeIndex+1][0]
    res = GRIDS[maxSizeIndex][0]
    x0 = int(utmWest / res) * res
    xmax = int(math.ceil(utmEast / res)) * res
    y0 = int(utmSouth / res) * res
    ymax = int(math.ceil(utmNorth / res)) * res
    gridLines = ''
    for i, x in enumerate(xrange(x0, xmax, res)):
        for j, y in enumerate(xrange(y0, ymax, res)):
            gridLines += makeGridLinesBlock(opts, thisFile, utmZone, utmLatBand, bounds, i, j, x, y, maxSizeIndex)

    region = getRegion(utmSW, utmNE, utmZone, utmLatBand)
    return makeNetworkLink(parentFile, thisFile, gridLines, region)


def makeGridLines(opts, parentFile, ullr):
    north, west, south, east = ullr

    gridLines = ''
    for zone in xrange(1, 61):
        zoneWest = -180 + 6 * (zone - 1)
        zoneEast = zoneWest + 6
        if zoneWest <= east and west <= zoneEast:
            if south <= 0:
                gridLines += makeGridLinesForZone(opts, parentFile, ullr, zone, isNorth=False)
            if north >= 0:
                gridLines += makeGridLinesForZone(opts, parentFile, ullr, zone, isNorth=True)
    return gridLines


def getZoneLines(opts, ullr):
    north, west, south, east = ullr
    zoneLines = ''

    # draw boundaries between utm zones
    for zone in xrange(1, 61):
        lon = -180 + 6 * (zone - 1)
        if west < lon < east:
            zoneLines += getLineString([south, lon], [north, lon], **ZONE_STYLE)

    # draw equator
    if south < 0 < north:
        zoneLines += getLineString([0, west], [0, east], **ZONE_STYLE)

    return zoneLines


def dosys(cmd):
    print cmd
    os.system(cmd)


def usngGrid(opts, boundsName, kmzName):
    global GRIDS
    GRIDS = [g for g in GRIDS if g[0] >= opts.minres]

    ullr = getUllrFromKml(boundsName)
    if opts.verbose:
        print >> sys.stderr, 'ullr:', ullr
    global outDirG
    outDirG = tempfile.mkdtemp()
    dosys('cp %s/corner.png %s' % (os.path.dirname(__file__), outDirG))
    topFile = os.path.join(outDirG, 'doc.kml')
    contents = ''
    contents += getZoneLines(opts, ullr)
    contents += makeGridLines(opts, topFile, ullr)
    writeFile(topFile, wrapKml(wrapFolder(contents)))

    kmzFullPath = os.path.abspath(kmzName)
    os.chdir(outDirG)
    if os.path.exists(kmzFullPath):
        dosys('rm -f %s' % kmzFullPath)
    dosys('zip -r %s doc.kml' % (kmzFullPath))
    dosys('zip -r %s *' % (kmzFullPath))


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <bounds.kml> <out.kmz>')
    parser.add_option('-m', '--minres',
                      type='int', default=50,
                      help='Minimum resolution to render [%default]')
    parser.add_option('-v', '--verbose',
                      action='store_true', default=False,
                      help='Turn on debugging output')
    opts, args = parser.parse_args()
    if len(args) != 2:
        parser.error('expected exactly 2 args')
    usngGrid(opts, args[0], args[1])

if __name__ == '__main__':
    main()
