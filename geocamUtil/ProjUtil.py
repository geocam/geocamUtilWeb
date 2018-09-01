#__BEGIN_LICENSE__
# Copyright (c) 2015, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The xGDS platform is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#__END_LICENSE__

import pyproj
import math

GEOD = pyproj.Geod(ellps='WGS84')


def get_projection(utm_zone, south):
    """
    Get a pyproj projection for WGS84 given the utm zone and south
    :param utm_zone:
    :param south:
    :return:
    """
    if not south:
        south_string = ''
    else:
        south_string = '+south'
    projection = pyproj.Proj("+proj=utm +zone=%s, %s +ellps=WGS84 +datum=WGS84 +units=m +no_defs" % (utm_zone, south_string))
    return projection


def ll_to_utm(longitude, latitude, projection):
    """
    Convert longitude latitude to UTM
    :param longitude:
    :param latitude:
    :param projection: the projection to use
    :return: tuple result, (easting, northing)
    """

    return projection(longitude, latitude)


def utm_to_ll(easting, northing, projection):
    """
    Convert easting, northing to longitude, latitude
    :param easting:
    :param northing:
    :param projection:
    :return: tuple result, (longitude, latitude)
    """

    return projection(easting, northing, inverse=True)


def norm2(point_1, point_2):
    """
    Using least squares to get a straight line distance.
    You could use easting,northing points for these calculations
    :param point_1:
    :param point_2:
    :return:
    """
    x_1, y_1 = point_1
    x_2, y_2 = point_2
    return math.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)


def distance_meters(lonLat1, lonLat2):
    """
    Calculate the distance in meters on a globe between two points
    :param lonLat1:
    :param lonLat2:
    :return: distance in meters
    """
    # GEOD.inv fails when Points are nearly equal
    if norm2(lonLat1, lonLat2) < 1e-5:
        return 0

    lon1, lat1 = lonLat1
    lon2, lat2 = lonLat2
    _az12, _az21, dist = GEOD.inv(lon1, lat1, lon2, lat2)
    return dist
