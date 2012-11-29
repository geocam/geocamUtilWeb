# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from geocamUtil import anyjson as json

from geocamUtil.models.ExtrasDotField import convertToDotDictRecurse


def loadConfig(path):
    f = open(path, 'r')
    j = json.load(f)
    return convertToDotDictRecurse(j)
