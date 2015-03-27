# __BEGIN_LICENSE__
#Copyright © 2015, United States Government, as represented by the 
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
# __END_LICENSE__

from geocamUtil import settings


def AuthUrlsContextProcessor(request):
    """
    Adds login and logout urls to the context.
    """
    if hasattr(settings, 'LOGIN_DEFAULT_NEXT_URL'):
        # deprecated. we originally chose LOGIN_DEFAULT_NEXT_URL because we did not know about LOGIN_REDIRECT_URL.
        loginSuffix = '?next=' + settings.LOGIN_DEFAULT_NEXT_URL
    elif hasattr(settings, 'LOGIN_REDIRECT_URL'):
        # LOGIN_REDIRECT_URL is the settings field that Django's auth module uses for this purpose
        # https://docs.djangoproject.com/en/dev/ref/settings/
        loginSuffix = '?next=' + settings.LOGIN_REDIRECT_URL
    else:
        loginSuffix = ''

    return {
        'login_url': settings.LOGIN_URL,
        'logout_url': settings.LOGOUT_URL,
        'login_url_with_next': settings.LOGIN_URL + loginSuffix
    }
