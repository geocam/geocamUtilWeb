# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

# stop pylint from warning that these variable docstrings are "useless"
# pylint: disable=W0105

import socket
from geocamUtil.SettingsUtil import getOrCreateArray

GEOCAM_UTIL_DELETE_TMP_FILE_WAIT_SECONDS = 60 * 60
"""
The age at which a geocamUtil.tempfiles file becomes "stale".  When
tempfiles detects a stale file in its directory it will be deleted.
"""

GEOCAM_UTIL_INSTALLER_USE_SYMLINKS = False

######################################################################
# GEOCAM_UTIL_SECURITY_* -- settings for geocamUtil.middleware.SecurityMiddleware

"""
You can find copious documentation for these settings with::

  from geocamUtil.middleware import SecurityMiddleware
  help(SecurityMiddleware)
"""

GEOCAM_UTIL_SECURITY_ENABLED = True
"""
If False, turn off all SecurityMiddleware security checks and
redirects.
"""

GEOCAM_UTIL_SECURITY_DEFAULT_POLICY = None
"""
The default security policy to which other rules are added.
"""

GEOCAM_UTIL_SECURITY_RULES = ()
"""
A tuple of rules that change the default security policy depending on
the URL pattern the request matches.
"""

GEOCAM_UTIL_SECURITY_TURN_OFF_SSL_WHEN_NOT_REQUIRED = False
"""
Controls what happens when users use SSL to connect to a URL where it is
not required.  If True, they will be redirected to the non-SSL version.
"""

GEOCAM_UTIL_SECURITY_REQUIRE_ENCRYPTED_PASSWORDS = True
"""
If True, only accept encrypted or hashed passwords.
"""

GEOCAM_UTIL_SECURITY_SECRET_URL_REGEX = None
"""
If the request path matches this regex and the security policy
permits 'secretUrl' authentication, the request is authenticated.
"""

GEOCAM_UTIL_SECURITY_DEPRECATED_BEHAVIOR = 'warn'
"""
Changes how geocamUtil responds to use of deprecated features.
"""

GEOCAM_UTIL_SECURITY_SSL_REQUIRED_BY_DEFAULT = True
"""
DEPRECATED. Use GEOCAM_UTIL_SECURITY_DEFAULT_POLICY sslRequired instead.
"""

GEOCAM_UTIL_SECURITY_LOGIN_REQUIRED_BY_DEFAULT = True
"""
DEPRECATED. Use GEOCAM_UTIL_SECURITY_DEFAULT_POLICY loginRequired instead.
"""

GEOCAM_UTIL_SECURITY_DEFAULT_CHALLENGE = 'django'
"""
DEPRECATED. Use GEOCAM_UTIL_SECURITY_DEFAULT_POLICY challenge instead.
"""

GEOCAM_UTIL_SECURITY_ACCEPT_AUTH_TYPES = ('basic',)
"""
DEPRECATED. Use GEOCAM_UTIL_SECURITY_DEFAULT_POLICY acceptAuthTypes instead.
"""

DIGEST_REALM = 'undefinedrealm'
"""
Realm to display to user when using the 'basic' challenge.

(Note: The name of the setting was chosen when it was used primarily
with HTTP digest authentication, which is no longer supported. We
avoided changing the name to keep backward compatibility.)
"""

GEOCAM_UTIL_LIVE_MODE = False
"""
If live mode is true, various live feed data can send inputs to site and
 more parts of the site will be visible.  Suggest expansion to include a
 list of services.

 IMPORTANT YOU MUST INCLUDE THIS IN siteSettings
 TEMPLATE_CONTEXT_PROCESSORS = (global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
     ...
     'geocamUtil.context_processors.SettingsContextProcessor.SettingsContextProcessor'
 """

# WARNING could NOT get pipeline compiler to compile gumby, so instead we have our own step in prep, prepcss.
# do not do this section
# GEOCAM_UTIL_PIPELINE_COMPILERS = ('pipeline_compass.compiler.CompassCompiler',  # this is for django-pipeline-compass
#                                   )
# """
# And you must add this to PIPELINE_COMPILERS in siteSettings
# PIPELINE_COMPILERS = ()
# PIPELINE_COMPILERS = PIPELINE_COMPILERS + geocamUtil.settings.GEOCAM_UTIL_PIPELINE_COMPILERS
# """
# end do not do section


"""
Set up pipeline for gumby.
"""
"""
Note the following for some reason does not work when only included here, so you must also have this in your siteSettings.py
PIPELINE_CSS = {}
PIPELINE_CSS.update(xgds_planner2.settings.XGDS_PLANNER_PIPELINE_CSS)
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_YUGLIFY_JS_ARGUMENTS = 'mangle:false --terminal'
PIPELINE_DISABLE_WRAPPER = True
PIPELINE_ENABLED = True
"""
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_YUGLIFY_JS_ARGUMENTS = 'mangle:false --terminal'
# PIPELINE_DISABLE_WRAPPER = True

GEOCAM_UTIL_PREPCSS_DIRS = ['gumby']
GEOCAM_UTIL_COMPRESSCSS_FILES = ['gumby/css/gumby.css']

BOWER_INSTALLED_APPS = getOrCreateArray('BOWER_INSTALLED_APPS')
BOWER_INSTALLED_APPS += ['underscore',
                         'modernizr=components-modernizr',
                         'jquery#3.1.1',
                         'jquery-ui',
                         'datatables=DataTables',
                         'datatables-select',
                         'jeditable',
                         'jqueryui-timepicker-addon=jQuery-Timepicker-Addon',
                         'jquery-validate',
                         'jeditable',
                         'gumby#master',
                         'bootstrap#v4.0.0-alpha.6',
                         'tether=https://github.com/HubSpot/tether.git',
                         'moment',
                         'moment-timezone',
                         'fontawesome',
                         ]

try:
    HOSTNAME = socket.gethostname()
except:
    HOSTNAME = 'localhost'

# set up a dictionary of the siteframes you will be working with.
# This is used by the Siteframe Choice form field
# XGDS_SITEFRAMES = {
#                    '10S': {  # ARC Marscape siteframe for testing
#                            'name': 'Ames',
#                            'east0': 582670.0,  # Easting
#                            'north0': 4141480.0,  # Northing
#                            'zone': '10S',
#                            'zoneNumber': 10,
#                            'axes': 'NED',
#                            'north': 'grid',
#                            'timezone': 'America/Los_Angeles'
#                            },
#                    }


# If you have a license for datatables editor then this can be true
GEOCAM_UTIL_DATATABLES_EDITOR = False

# default to earth
GEOCAM_UTIL_BODY_RADIUS_METERS = 6371010