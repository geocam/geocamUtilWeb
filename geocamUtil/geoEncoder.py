from django.core.serializers.json import DjangoJSONEncoder

from django.db.models.fields.files import ImageFieldFile
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Point, LineString, Polygon


class GeoDjangoEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Polygon):
            result = obj.coords[0]
            return result
        if isinstance(obj, GEOSGeometry):
            result = obj.json()
            return result
        if isinstance(obj, ImageFieldFile):
            try:
                return obj.url
            except ValueError, e:
                return ''
        return super(GeoDjangoEncoder, self).default(obj)
