# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os
import re
from glob import glob

from PIL import Image
from django.conf import settings

ICON_URL_CACHE = {}
ICON_SIZE_CACHE = {}


def cacheIcons(d, mediaDir=settings.MEDIA_ROOT, mediaUrl=settings.MEDIA_URL):
    paths = glob('%s/*' % d)
    for p in paths:
        iconPrefix, iconExt = os.path.splitext(os.path.basename(p))
        if iconExt.lower() not in ('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.gif'):
            continue
        im = Image.open(p)
        ICON_SIZE_CACHE[iconPrefix] = list(im.size)
        ICON_URL_CACHE[iconPrefix] = re.sub(mediaDir, mediaUrl, p)


def getIconSize(iconPrefix):
    return ICON_SIZE_CACHE[iconPrefix]


def getIconUrl(iconPrefix):
    return ICON_URL_CACHE[iconPrefix]

# for export
import rotate
import svg
