# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from geocamUtil.middleware.SecurityMiddleware import requestIsSecure
from geocamAware import settings
import urllib

def getAccountWidget(request):
    if request.user.is_authenticated():
        """
        accountWidget = ('<a href="%(SCRIPT_NAME)saccounts/profile">%(username)s</a> <a href="%(SCRIPT_NAME)saccounts/logout/">logout</a>'
                         % dict(SCRIPT_NAME=settings.SCRIPT_NAME, username=request.user.username))
        """
        accountWidget = ('<a href="%(SCRIPT_NAME)saccounts/profile">%(username)s</a> | <a href="%(SCRIPT_NAME)saccounts/logout/">Logout</a>'
                        % dict(SCRIPT_NAME=settings.SCRIPT_NAME, username=request.user.username))
        
    else:
        path = request.get_full_path()
        if not requestIsSecure(request):
            path += '?protocol=http' # redirect back to http after login
            
        """
        accountWidget = ('<b>guest</b> <a href="%(SCRIPT_NAME)saccounts/register">register</a> <a href="%(SCRIPT_NAME)saccounts/login/?next=%(path)s">login</a>'
                         % dict(SCRIPT_NAME=settings.SCRIPT_NAME,
                                path=urllib.quote(path)))
        """
        
        accountWidget = ('<div id="accountwidget"><a id="login_button" href="%(SCRIPT_NAME)saccounts/login?next=%(path)s">Login</a> | <a id="join_button" href="%(SCRIPT_NAME)saccounts/register">Join</a></div>'
                        % dict(path=request.path, SCRIPT_NAME=settings.SCRIPT_NAME, username=request.user.username))
                                
    return accountWidget