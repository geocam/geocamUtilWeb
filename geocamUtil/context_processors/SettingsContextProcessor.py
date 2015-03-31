# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from geocamUtil import settings


def SettingsContextProcessor(request):
    """
    Adds various settings to the context
    """
    return {
        'LIVE_MODE': settings.GEOCAM_UTIL_LIVE_MODE,
        'EXTERNAL_URL': settings.EXTERNAL_URL
    }
