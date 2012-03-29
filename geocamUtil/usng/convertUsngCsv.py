#!/usr/bin/env python

"""
Takes as input a CSV file in the format:

37 46 29.2080,-122 25 08.1336,San Francisco
37 27 13.8132,-122 10 55.7184,Menlo Park

And outputs CSV in the format:

10S EG 51172 80985,San Francisco
10S EG 72335 45533,Menlo Park

Optionally outputs a KML file of placemarks as well, where the
placemark descriptions include USNG coordinates.
"""

import csv

from geocamUtil.usng import usng
from geocamUtil import KmlUtil


def parseDegMinSec(val):
    valDeg, valMin, valSec = val.split(' ')
    sgn = -1 if float(valDeg) < 0 else 1
    return sgn * (abs(float(valDeg))
                  + float(valMin) / 60.0
                  + float(valSec) / 3600.0)


def convertUsngCsv(opts, inPath):
    inFile = file(inPath, 'r')
    inLines = csv.reader(inFile)
    coords = []
    for latDms, lonDms, name in inLines:
        lat = parseDegMinSec(latDms)
        lon = parseDegMinSec(lonDms)
        easting, northing, zoneNumber, zoneLetter = usng.LLtoUTM(lat, lon)
        easting += opts.eastOffset
        northing += opts.northOffset
        usngCoords = usng.UTMtoUSNG(easting, northing, zoneNumber, zoneLetter, precision=5)
        print usngCoords, '    ', name
        clat, clon = usng.UTMtoLL(easting, northing, zoneNumber, zoneLetter)
        coords.append((clat, clon, name, usngCoords))

    if opts.kml:
        kbits = []
        kbits.append('<Folder>\n')
        for lat, lon, name, usngCoords in coords:
            kbits.append("""
<Placemark>
  <name>%(name)s</name>
  <description>%(usngCoords)s</description>
  <Point>
    <coordinates>%(lon)s,%(lat)s</coordinates>
  </Point>
</Placemark>
""" % dict(lat=lat, lon=lon, name=name,
           usngCoords=usngCoords))
        kbits.append('</Folder>')
        text = ''.join(kbits)
        file(opts.kml, 'w').write(KmlUtil.wrapKml(text))


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <in.csv>')
    parser.add_option('--eastOffset',
                      type='float', default=0,
                      help='Offset to add to easting values for datum correction (meters)')
    parser.add_option('--northOffset',
                      type='float', default=0,
                      help='Offset to add to northing values for datum correction (meters)')
    parser.add_option('--kml',
                      help='Filename for KML output')
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error('expected exactly 1 arg')
    inPath = args[0]
    convertUsngCsv(opts, inPath)

if __name__ == '__main__':
    main()
