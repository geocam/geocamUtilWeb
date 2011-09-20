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

######################################################################
# GEOCAM_UTIL_SECURITY_* -- settings for geocamUtil.middleware.SecurityMiddleware

GEOCAM_UTIL_SECURITY_ENABLED = True
"""
If False, turn off all SecurityMiddleware security checks and
redirects.  This flag is handy because taking SecurityMiddleware
out of settings.MIDDLEWARE_CLASSES altogether will cause errors if you're
using any per-url flags.
"""

GEOCAM_UTIL_SECURITY_SSL_REQUIRED_BY_DEFAULT = True
"""
If True, SSL connections are required by default for all urls.
You can override this setting on a per-url basis by setting the
'sslRequired' flag.
"""

GEOCAM_UTIL_SECURITY_TURN_OFF_SSL_WHEN_NOT_REQUIRED = False
"""
Controls what happens when users use SSL to connect to a URL where it is
not required.  If True, they will be redirected to the non-SSL version.
"""

GEOCAM_UTIL_SECURITY_LOGIN_REQUIRED_BY_DEFAULT = True
"""
Set to True, False, or 'write'.  If 'write', login is required to access
urls that don't have the 'readOnly' flag.  You can override this setting
on a per-url basis by setting the 'loginRequired' flag.
"""

GEOCAM_UTIL_SECURITY_DEFAULT_CHALLENGE = 'django'
"""
Set to 'django', 'digest', or 'basic'.  Controls what challenge the
server sends to a non-authenticated user who requests a page that
requires authentication.

If 'django', use the default Django challenge, an HTML form asking for
user/password.  If the user successfully logs in their credentials will
be stored in a session cookie until they log out.

If 'digest' or 'basic', send an HTTP digest or basic authentication
challenge, an HTTP response 401 with a header that causes compatible
browsers to prompt the user for a username and password. If the user
successfully logs in the browser will cache their credentials until it
is restarted.  'basic' sends the password unencrypted so it must only be
used over SSL connections.

You can override this setting on a per-url basis by setting the
'challenge' flag.
"""

GEOCAM_UTIL_SECURITY_ACCEPT_AUTH_TYPES = ('digest', 'basic')
"""
List of types of authentication that should be accepted (in addition to
the built-in Django authentication, which is always accepted).

Options are: 'digest', 'basic'.  See GEOCAM_UTIL_SECURITY_DEFAULT_CHALLENGE
for more information.

You can override this setting on a per-url basis by setting the
'acceptAuthTypes' flag.
"""

GEOCAM_UTIL_SECURITY_REQUIRE_ENCRYPTED_PASSWORDS = True
"""
If True, only accept encrypted or hashed passwords.  This will cause the
'django' password form and 'basic' credentials to be rejected unless
they are posted via SSL.  It has no effect on 'digest' which uses hashed
credentials.
"""
