# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from geocamUtil import settings


def AuthUrlsContextProcessor(request):
    """
    Adds login and logout urls to the context.
    """
    if hasattr(settings, 'LOGIN_DEFAULT_NEXT_URL'):
        loginSuffix = '?next=' + settings.LOGIN_DEFAULT_NEXT_URL
    else:
        loginSuffix = ''

    return {
        'login_url': settings.LOGIN_URL,
        'logout_url': settings.LOGOUT_URL,
        'login_url_with_next': settings.LOGIN_URL + loginSuffix
    }
