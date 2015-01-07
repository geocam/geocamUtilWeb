# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

# stop pylint from warning that these variable docstrings are "useless"
# pylint: disable=W0105

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

GEOCAM_UTIL_PIPELINE_COMPILERS = (
    'pipeline_compass.compiler.CompassCompiler',
)
"""
And you must add this to PIPELINE_COMPILERS in siteSettings
PIPELINE_COMPILERS = ()
PIPELINE_COMPILERS = PIPELINE_COMPILERS + geocamUtil.settings.GEOCAM_UTIL_PIPELINE_COMPILERS
"""


"""
Set up pipeline for gumby.
"""
GEOCAM_UTIL_PIPLINE_CSS = {'gumby': {'source_filenames': (#'external/gumby/sass/var/_settings.scss',
#                                                           'external/gumby/sass/var/_lists.scss',
#                                                           'external/gumby/sass/var/icons/_entypo-icon-list.scss',
                                                          #'external/gumby/sass/var/icons/_entypo.scss',
                                                          #'external/gumby/sass/extensions/sassy-math/stylesheets/*.scss',
                                                          #'external/gumby/sass/extensions/modular-scale/stylesheets/*.scss',
                                                          #'external/gumby/sass/functions/*.scss',
                                                          #'external/gumby/sass/ui/*.scss',
                                                          #'external/gumby/sass/*.scss',
                                                          'external/gumby/sass/gumby.scss',
                                                          'external/gumby/css/*.css',
                                                          'external/gumby/*.json'
                                                          'external/gumby/config.rb',
                                                          ),
                                     'output_filename': 'external/gumby/css/gumby.css'
                                     }
                           }

PIPELINE_COMPASS_ARGUMENTS = '--debug-info -c build/static/external/gumby/config.rb'  # default: ''

