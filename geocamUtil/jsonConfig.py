# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from geocamUtil import anyjson as json

from geocamUtil.models.ExtrasDotField import convertToDotDictRecurse


def loadConfig(path):
    f = open(path, 'r')
    j = json.load(f)
    return convertToDotDictRecurse(j)
