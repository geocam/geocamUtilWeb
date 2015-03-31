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

from geocamUtil.middleware.security import requestIsSecure
from geocamUtil import settings


def getAccountWidget(request):
    if request.user.is_authenticated():
        accountWidget = ('<a href="%(SCRIPT_NAME)saccounts/profile">%(username)s</a>&nbsp;<a href="%(SCRIPT_NAME)saccounts/logout/">Logout</a>'
                         % dict(SCRIPT_NAME=settings.SCRIPT_NAME, username=request.user.username))
    else:
        path = request.get_full_path()
        if requestIsSecure(request):
            path += '?protocol=http'  # redirect back to http after login

        accountWidget = ('<div id="accountwidget"><a id="login_button" href="%(SCRIPT_NAME)saccounts/login?next=%(path)s">Login</a> | <a id="join_button" href="%(SCRIPT_NAME)saccounts/register">Join</a></div>'
                         % dict(path=path,
                                SCRIPT_NAME=settings.SCRIPT_NAME,
                                username=request.user.username))

    return accountWidget
