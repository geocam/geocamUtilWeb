# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the
#Administrator of the National Aeronautics and Space Administration.
#All rights reserved.
# __END_LICENSE__
# __BEGIN_APACHE_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
#
#The xGDS platform is licensed under the Apache License, Version 2.0 
#(the "License"); you may not use this file except in compliance with the License. 
#You may obtain a copy of the License at 
#http://www.apache.org/licenses/LICENSE-2.0.
#
#Unless required by applicable law or agreed to in writing, software distributed 
#under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
#CONDITIONS OF ANY KIND, either express or implied. See the License for the 
#specific language governing permissions and limitations under the License.
# __END_APACHE_LICENSE__

import os
import re
from glob import glob

from PIL import Image
from django.conf import settings

ICON_URL_CACHE = {}
ICON_SIZE_CACHE = {}


def cacheIcons(d, staticDir=settings.STATIC_ROOT, staticUrl=settings.STATIC_URL):
    paths = glob('%s/*' % d)
    for p in paths:
        iconPrefix, iconExt = os.path.splitext(os.path.basename(p))
        if iconExt.lower() not in ('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.gif'):
            continue
        im = Image.open(p)
        ICON_SIZE_CACHE[iconPrefix] = list(im.size)
        ICON_URL_CACHE[iconPrefix] = re.sub(staticDir, staticUrl, p)


def getIconSize(iconPrefix):
    return ICON_SIZE_CACHE[iconPrefix]


def getIconUrl(iconPrefix):
    return ICON_URL_CACHE[iconPrefix]

# for export
import rotate
import svg
