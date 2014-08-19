# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import re
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.http import HttpResponse


def wrapKmlHttp(text):
    wrapped = wrapKml(text)
    return ("""HTTP/1.0 200 OK\r
Content-type: application/vnd.google-earth.kml+xml
Expires: -1

%s
""" % wrapped)


def wrapKmlDjango(text):
    return djangoResponse(wrapKml(text))


def djangoResponse(wrappedText):
    return HttpResponse(wrappedText, mimetype='application/vnd.google-earth.kml+xml')


def wrapKml(text, docId=None):
    if docId:
        text = re.sub(r'^<(\w+)>', '<\\1 id="%s">' % docId, text)
    return ("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2"
     xmlns:gx="http://www.google.com/kml/ext/2.2"
     xmlns:kml="http://www.opengis.net/kml/2.2"
     xmlns:atom="http://www.w3.org/2005/Atom">
  %s
</kml>
""" % text)


def wrapKmlDocument(text, docId=None):
    if docId:
        return wrapKml("""
  <Document id="%(docId)s">
    <name>%(docId)s</name>
    %(text)s
  </Document>
""" % dict(docId=docId, text=text))
    else:
        return wrapKml("""
  <Document>
    %s
  </Document>
""" % text)


def _makeGetter(userSpec, fieldNames, defaultValue):
    if callable(userSpec):
        return userSpec
    if userSpec is not None:
        fieldNames = [userSpec]

    def getter(key, value):
        result = None
        for fieldName in fieldNames:
            if fieldName is 'key':
                result = key
                break
            if hasattr(value, '__getitem__'):
                try:
                    result = value[fieldName]
                    break
                except (TypeError, KeyError):
                    pass
            else:
                result = getattr(value, fieldName, None)
                if result:
                    break
        if result is None:
            return defaultValue
        if callable(result):
            result = result()
        return result

    return getter


def markers(collection,
            name=None,
            description=None,
            longitude=None,
            latitude=None,
            styleUrl=None):
    nameFn = _makeGetter(name, ['name', 'key'], None)
    descriptionFn = _makeGetter(description, ['description'], None)
    longitudeFn = _makeGetter(longitude, ['longitude', 0], None)
    latitudeFn = _makeGetter(latitude, ['latitude', 1], None)
    styleUrlFn = _makeGetter(styleUrl, ['styleUrl'], None)

    dictLike = hasattr(collection, 'keys')
    markerText = StringIO()
    for index, item in enumerate(collection):
        if dictLike:
            key = item
            value = collection[item]
        else:
            key = index
            value = item

        nameVal = nameFn(key, value)
        descriptionVal = descriptionFn(key, value)
        longitudeVal = longitudeFn(key, value)
        assert longitudeVal is not None
        latitudeVal = latitudeFn(key, value)
        assert latitudeVal is not None
        styleUrlVal = styleUrlFn(key, value)

        markerText.write('<Placemark>\n')
        if nameVal not in ('', u'', None):
            markerText.write('  <name>%s</name>\n' % nameVal)
        if descriptionVal not in ('', u'', None):
            markerText.write('  <description>%s</description>\n' % descriptionVal)
        if styleUrlVal not in ('', u'', None):
            markerText.write('  <styleUrl>%s</styleUrl>\n' % styleUrlVal)
        markerText.write('  <Point>\n')
        markerText.write('    <coordinates>%s,%s</coordinates>\n' % (longitudeVal, latitudeVal))
        markerText.write('  </Point>\n')
        markerText.write('</Placemark>\n')
    return markerText.getvalue()

def makeStyle(id, iconUrl=None, iconScale=None, iconColor=None, lineColor=None, lineWidth=None, polyColor=None, polyFill=1, polyOutline=1):
    """
    Create a style block.  This will fill in any and all of the style sections based on parameters given.
    Note that polyStyle requires a color.
    """
    result = ('''
<Style id="%s">''' % id )
    if iconUrl:
        result = result + ('''
    <IconStyle>
        <Icon>
            <href>%s</href>''' % iconUrl)
        if iconScale:
            result = result + ('''
            <scale>%d</scale>''' % iconScale)
        result = result + ('''
        </Icon>''')
        if iconColor:
            result = result + ('''
        <color>%s</color>''' % iconColor)
        result = result + ('''  
    </IconStyle>''')
        
    if lineColor or lineWidth:
        result = result + ('''
    <LineStyle>''')
        if lineColor:
            result = result + ('''
        <color>%s</color>''' % lineColor)
        if lineWidth:
            result = result + ('''
        <width>%d</width>''' % lineWidth)
        result = result + ('''
    </LineStyle>''')
    if polyColor:
        result = result + ('''
    <PolyStyle>
        <color>%s</color>
        <fill>%d</fill>
        <outline>%d</outline>
    </PolyStyle>''' % (polyColor, polyFill, polyOutline))
    result = result + ('''
</Style>''')
    return result