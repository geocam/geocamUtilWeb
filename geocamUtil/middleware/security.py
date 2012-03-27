# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__


import re
import sys
import traceback
import base64
import operator

from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect, \
     HttpResponsePermanentRedirect, HttpResponseForbidden, \
     HttpResponseServerError, get_host
from django.core.urlresolvers import resolve
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.http import urlquote

from geocamUtil import settings

# stop pylint from warning about too many return statements; it's good
# style in this case
# pylint: disable=R0911


POLICY_FIELDS = ('sslRequired',
                 'loginRequired',
                 'challenge',
                 'acceptAuthTypes',
                 'forbidden')


def requestIsSecure(request):
    if request.is_secure():
        return True

    # Handle forwarded SSL (used at Webfaction)
    if 'HTTP_X_FORWARDED_SSL' in request.META:
        return request.META['HTTP_X_FORWARDED_SSL'] == 'on'

    if 'HTTP_X_SSL_REQUEST' in request.META:
        return request.META['HTTP_X_SSL_REQUEST'] == '1'

    return False


def getDefaultSecurityPolicy():
    defaults = {'sslRequired': settings.GEOCAM_UTIL_SECURITY_SSL_REQUIRED_BY_DEFAULT,
                'loginRequired': settings.GEOCAM_UTIL_SECURITY_LOGIN_REQUIRED_BY_DEFAULT,
                'challenge': settings.GEOCAM_UTIL_SECURITY_DEFAULT_CHALLENGE,
                'acceptAuthTypes': settings.GEOCAM_UTIL_SECURITY_ACCEPT_AUTH_TYPES,
                'forbidden': False}
    if settings.GEOCAM_UTIL_SECURITY_DEFAULT_POLICY is not None:
        defaults.update(settings.GEOCAM_UTIL_SECURITY_DEFAULT_POLICY)
    return defaults


def all_(lst):
    # re-implement all() builtin to support Python 2.4 (yay!)
    return reduce(operator.__and__, lst, True)


def getSecurityPolicy(securityTags):
    policy = getDefaultSecurityPolicy()
    for rule in settings.GEOCAM_UTIL_SECURITY_RULES:
        if all_([tag in securityTags for tag in rule['tags']]):
            policy.update(rule.get('policy', {}))
            if rule.get('break', False):
                break
    return policy


def deprecateCheck(msg):
    b = settings.GEOCAM_UTIL_SECURITY_DEPRECATED_BEHAVIOR
    assert b in ('ok', 'warn', 'disable', 'error')
    if b is 'ok':
        return (True, None)
    else:
        print >> sys.stderr, 'geocamUtil.middleware.SecurityMiddleware: Using deprecated feature: %s' % msg
        if b is 'warn':
            return (True, None)
        elif b is 'disable':
            return (False, None)
        elif b is 'error':
            return (False, HttpResponseServerError('<h1>HTTP 500 Server Error</h1>'))


# http://stackoverflow.com/questions/2164069/best-way-to-make-djangos-login-required-the-default
# http://stackoverflow.com/questions/1548210/how-to-force-the-use-of-ssl-for-some-url-of-my-django-application
class SecurityMiddleware(object):
    """
    SecurityMiddleware helps to standardize the security policy across a
    site containing multiple apps in a way that's more scalable than
    adding decorators to each view.  Its behavior is very flexible and
    is controlled by the site's settings.

    Installation
    ============

     * Install dependencies::

         pip install django-digest python-digest

     * Install `geocamUtil` in your `PYTHONPATH`.

     * Add the middleware to your `settings.py`::

         MIDDLEWARE_CLASSES = (
           ...
           'geocamUtil.middleware.SecurityMiddleware',
           ...
         )

    Getting Started
    ===============

    Begin by setting your default security policy in `settings.py`. For
    example::

      GEOCAM_UTIL_SECURITY_DEFAULT_POLICY = {
          'sslRequired': False,
          'loginRequired': True,
          'challenge': 'django'
      }

    The middleware will apply this policy to all views unless otherwise
    specified.

    Now suppose we want to change the policy for some views. Begin by
    specifying the `securityTags` field in the extra options section of
    our URL patterns in `urls.py`, like so::

      (r'^private.html$', views.private,
       {'securityTags': ['sensitive']}),

      (r'^accounts/login/$', 'django.contrib.auth.views.login',
       {'securityTags': ['isLogin']}),

      (r'^foo.kml$', views.foo,
       {'securityTags': ['kml', 'readOnly']}),

      (r'^bar.kml$', views.foo,
       {'securityTags': ['kml']})

    The tag names you choose are arbitrary and should describe
    security-related facts about your views.  In this case, we chose
    tags with the following meanings:

      * `sensitive`: The view returns sensitive data, and therefore
        might need more protection.

      * `isLogin`: The view is an authentication challenge. Generally
        challenges should not be protected, to avoid causing a redirect
        loop.

      * `kml`: The view returns a KML file that may need to be loaded by
        the Google Earth desktop client, which does not support our
        default 'django' authentication challenge.

      * `readOnly`: The view does not change the application state, and
        therefore might need less protection.

    Now that we have tags on views, we can condition our security policy
    on the tags by adding rules to `settings.py`, like so:

      GEOCAM_UTIL_SECURITY_RULES = (

          # require SSL for sensitive information
          {
              'tags': ['sensitive'],
              'policy': {
                  'sslRequired': True
              },
              # if this rule matches, disable checking later rules
              'break': True
          },

          # don't require login to see login pages!
          {
              'tags': ['isLogin'],
              'policy': {
                  'loginRequired': False
              },
              'break': True
          },

          # use challenge compatible with Google Earth desktop client
          {
              'tags': ['kml'],
              'policy': {
                  'challenge': 'basic'
              }
          },

          # allow users to visit read-only pages without login
          {
              'tags': ['readOnly'],
              'policy': {
                  'loginRequired': False
              }
          }
      )

    When a request comes in, after URL routing, SecurityMiddleware
    intercepts it and examines the `securityTags` of the matching URL
    pattern. A security rule matches the request if *all* of its `tags`
    are found in the `securityTags`.

    To determine the policy for the request, SecurityMiddleware starts
    with the default policy and checks the rules in order. The `policy`
    values in each matching rule overwrite values specified in the
    default policy or previous rules. If a matching rule has the `break`
    field set, that finalizes the policy -- SecurityMiddleware will not
    evaluate later rules.

    Design Goals
    ============

    The initial goal of SecurityMiddleware was to enable building sites
    that are "secure by default" by allowing the site admin to specify a
    default security policy. Django's built-in view decorator security
    setup is always "open by default", which makes it very easy to
    accidentally leave some views unprotected--particularly when novice
    developers add new views.

    We found that attaching security meta-data to URL patterns
    centralized our security setup and made it easy to quickly scan the
    different settings for a large number of views at once. In Django's
    default setup, security settings are specified as a decorators
    attached to view functions.  Since each view function can be a large
    chunk of code, and the functions are more likely to be scattered
    across several files, it's difficult to get an overview of the
    security setup.

    As we scaled up our sites to include many reusable apps that defined
    their own views and URL patterns, we found it was important to
    separate security-related *facts* about views (the `securityTags`
    field), specified at the app level, from security *policies*,
    specified in the site settings.

    This separation makes it easy for a site admin to tweak their site's
    security policy, even specifying different policies for different
    views within a single installed app, without modifying the app
    itself. The tag and rule model allows a great deal of flexibility
    with fairly simple settings.

    The following resources helped to inspire the initial implementation
    of SecurityMiddleware:

      * http://stackoverflow.com/questions/2164069/best-way-to-make-djangos-login-required-the-default

      * http://stackoverflow.com/questions/1548210/how-to-force-the-use-of-ssl-for-some-url-of-my-django-application

    Reference
    =========

    Policy Fields
    ~~~~~~~~~~~~~

    Policy fields can be specified in any of three places:

     * In `settings.GEOCAM_UTIL_SECURITY_DEFAULT_POLICY`.

     * In the `policy` field of rules contained in
       `settings.GEOCAM_UTIL_SECURITY_RULES`. The `policy` values in
       matching rules override those in the default policy and earlier
       rules.

     * DEPRECATED: In the extra options section of URL patterns.  This
       overrides both the default policy and the rules. Using this
       feature makes it makes it more difficult to change security
       policy at the site level without modifying individual apps.

    `sslRequired`
    -------------

    Default: `True`

    If True, an SSL connection is required. This will trigger a redirect
    if the current connection is not SSL.

    Using SSL throughout your site is an excellent way to avoid subtle
    security problems, so this option is on by default.

    `loginRequired`
    ---------------

    Default: `True`

    If True, login is required. This will trigger an authentication
    challenge if the current connection is not authenticated.

    Requiring login improves security, so this option is on by default.

    DEPRECATED FEATURE: If @loginRequired is set to the string 'write',
    login is required to access views that don't have the @readOnly field
    set in the extra options section of their URL pattern.

    `challenge`
    -----------

    Default: `django`

    Set to `django`, `digest`, or `basic`.  Controls what challenge the
    server sends to a non-authenticated user who requests a page that
    requires authentication.

    If `django`, use the default challenge of the `django.contrib.auth`
    app, an HTTP 200 "ok" response containing an HTML form asking for
    user/password.  If the user successfully logs in their credentials
    will be stored in a session cookie until they log out.

    If `digest` or `basic`, send an HTTP digest or basic authentication
    challenge, an HTTP 401 "forbidden" response with a header that
    causes compatible browsers to prompt the user for a username and
    password. If the user successfully logs in the browser will cache
    their credentials until it is restarted.  `basic` sends the password
    unencrypted so it must only be used over SSL connections.

    `acceptAuthTypes`
    -----------------

    Default: `('digest', 'basic')`

    List of types of authentication that should be accepted (in addition
    to the built-in Django authentication, which is always accepted unless
    the `forbidden` flag is set).

    Options are: `digest`, `basic`, `secretUrl`.

    `forbidden`
    -----------

    Default: `False`

    If True, always return a 401 forbidden response. Do not accept any
    authentication.

    Generally, you would use this field in the policy rules to lock out
    particular views you don't want users to have access to.

    Settings
    ~~~~~~~~

    These variables can be specified in the site's Django settings.

    `GEOCAM_UTIL_SECURITY_ENABLED`
    ------------------------------

    If False, turn off all SecurityMiddleware security checks and
    redirects.  This flag is handy because taking SecurityMiddleware out
    of settings.MIDDLEWARE_CLASSES altogether will cause errors if
    you're putting SecurityMiddleware-specific fields in the extra
    options section of your URL patterns.

    `GEOCAM_UTIL_SECURITY_DEFAULT_POLICY`
    -------------------------------------

    The default policy to which other rules are added. A dict that
    includes the `policy fields`_ described above. See the `Getting
    Started`_ section for an example.

    For backward compatibility, if this parameter is not specified, the
    default policy values are the following::

      {
          'sslRequired': settings.GEOCAM_UTIL_SECURITY_SSL_REQUIRED_BY_DEFAULT,
          'loginRequired': settings.GEOCAM_UTIL_SECURITY_LOGIN_REQUIRED_BY_DEFAULT,
          'challenge': settings.GEOCAM_UTIL_SECURITY_DEFAULT_CHALLENGE,
          'acceptAuthTypes': settings.GEOCAM_UTIL_SECURITY_ACCEPT_AUTH_TYPES,
          'forbidden': False
      }

    `GEOCAM_UTIL_SECURITY_RULES`
    ----------------------------

    A tuple of rules that specify how the security policy changes based
    on the `securityTags` field in URL patterns. See the `Getting
    Started`_ section for an example.

    `GEOCAM_UTIL_SECURITY_TURN_OFF_SSL_WHEN_NOT_REQUIRED`
    -----------------------------------------------------

    Default: `False`

    Controls what happens when users use SSL to connect to a URL where it
    is not required.  If True, they will be redirected to the non-SSL
    version.

    This option may improve performance but reduces security, so it is
    off by default.

    `GEOCAM_UTIL_SECURITY_REQUIRE_ENCRYPTED_PASSWORDS`
    --------------------------------------------------

    Default: `True`

    If True, only accept encrypted or hashed passwords.  This will cause the
    `django` password form and `basic` credentials to be rejected unless
    they are posted via SSL.  It has no effect on `digest` which uses hashed
    credentials.

    This option helps you catch and fix cases when you are passing passwords
    over the net in cleartext, so it is on by default.

    `GEOCAM_UTIL_SECURITY_SECRET_URL_REGEX`
    ---------------------------------------

    If the `acceptAuthTypes` field contains `secretUrl` and the request
    path matches this regex, the request is considered to be
    authenticated.

    Secret URL authentication is not very secure and should only be used
    for low-security views when other authentication types are not
    available.

    The value of this setting is sensitive information and it should
    never be checked into version control!

    `GEOCAM_UTIL_SECURITY_DEPRECATED_BEHAVIOR`
    ------------------------------------------

    Default: `'warn'`

    Changes how geocamUtil responds to use of deprecated features:

     * `ok`: Enable deprecated features with no warning.

     * `warn`: Enable deprecated features and print a warning in the
       error log.

     * `disable`: Disable deprecated features and print a warning in the
       error log.

     * `error`: Cause a fatal error.

    `GEOCAM_UTIL_SECURITY_SSL_REQUIRED_BY_DEFAULT`
    ----------------------------------------------

    DEPRECATED. Use `GEOCAM_UTIL_SECURITY_DEFAULT_POLICY['sslRequired']`
    instead.

    `GEOCAM_UTIL_SECURITY_LOGIN_REQUIRED_BY_DEFAULT`
    ------------------------------------------------

    DEPRECATED. Use
    `GEOCAM_UTIL_SECURITY_DEFAULT_POLICY['loginRequired']` instead.

    `GEOCAM_UTIL_SECURITY_DEFAULT_CHALLENGE`
    ----------------------------------------

    DEPRECATED. Use `GEOCAM_UTIL_SECURITY_DEFAULT_POLICY['challenge']`
    instead.

    `GEOCAM_UTIL_SECURITY_ACCEPT_AUTH_TYPES`
    ----------------------------------------

    DEPRECATED. Use
   `GEOCAM_UTIL_SECURITY_DEFAULT_POLICY['acceptAuthTypes']` instead.
    """

    def __init__(self):
        if 'digest' in settings.GEOCAM_UTIL_SECURITY_ACCEPT_AUTH_TYPES:
            import django_digest
            self._digestAuthenticator = django_digest.HttpDigestAuthenticator()

    # http://djangosnippets.org/snippets/243/
    def _basicAuthenticate(self, request):
        # require SSL for basic auth -- avoid clients sending passwords in cleartext
        if not requestIsSecure(request) and settings.GEOCAM_UTIL_SECURITY_REQUIRE_ENCRYPTED_PASSWORDS:
            return False

        if 'HTTP_AUTHORIZATION' not in request.META:
            return False

        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) != 2:
            return False

        if auth[0].lower() != "basic":
            return False

        uname, passwd = base64.b64decode(auth[1]).split(':')
        user = authenticate(username=uname, password=passwd)
        if user == None:
            return False

        if not user.is_active:
            return False

        request.user = user
        return True

    def _basicChallenge(self, request):
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % settings.DIGEST_REALM
        return response

    def _djangoAuthenticate(self, request):
        return request.user.is_authenticated()

    def _djangoChallenge(self, request):
        loginUrlWithoutScriptName = '/' + settings.LOGIN_URL[len(settings.SCRIPT_NAME):]
        loginTuple = resolve(loginUrlWithoutScriptName)
        loginViewKwargs = loginTuple[2]
        sslRequired = loginViewKwargs.get('sslRequired', settings.GEOCAM_UTIL_SECURITY_REQUIRE_ENCRYPTED_PASSWORDS)
        if sslRequired and not requestIsSecure(request):
            # ssl required for login -- redirect to https and then back
            loginUrl = re.sub('^http:', 'https:', request.build_absolute_uri(settings.LOGIN_URL))
            path = request.get_full_path() + '?protocol=http'
        else:
            # default -- don't bother with protocol and hostname
            loginUrl = settings.LOGIN_URL
            path = request.get_full_path()
        url = '%s?%s=%s' % (loginUrl, REDIRECT_FIELD_NAME, urlquote(path))
        return HttpResponseRedirect(url)

    def _digestAuthenticate(self, request):
        return self._digestAuthenticator.authenticate(request)

    def _digestChallenge(self, request):
        return self._digestAuthenticator.build_challenge_response()

    def _secretUrlAuthenticate(self, request):
        regex = settings.GEOCAM_UTIL_SECURITY_SECRET_URL_REGEX
        assert (regex is not None), 'using secretUrl authentication without specifying settings.GEOCAM_UTIL_SECURITY_SECRET_URL_REGEX'
        return (regex.search(request.path) is not None)

    def process_view(self, request, viewFunc, viewArgs, viewKwargs):
        if not settings.GEOCAM_UTIL_SECURITY_ENABLED:
            # delete security-related extra options to avoid later errors
            for field in ('securityTags', 'readOnly') + POLICY_FIELDS:
                viewKwargs.pop(field, None)
            # let request through
            return None

        securityTags = viewKwargs.pop('securityTags', [])
        policy = getSecurityPolicy(securityTags)

        # deprecated: implement special behavior when loginRequired='write'
        if policy['loginRequired'] == 'write':
            ok, response = deprecateCheck('loginRequired special value "write"')
            if response:
                return response
        if 'readOnly' in viewKwargs:
            ok, response = deprecateCheck('"readOnly" field specified in URL extra options')
            if response:
                return response

            if ok:
                readOnly = viewKwargs.pop('readOnly', False)
                if policy['loginRequired'] == 'write':
                    policy['loginRequired'] = not readOnly

        # deprecated: implement policy override based on URL extra options
        for field in POLICY_FIELDS:
            if field in viewKwargs:
                ok, response = deprecateCheck('"%s" field specified in URL extra options' % field)
                if response:
                    return response

                val = viewKwargs.pop(field, None)
                if ok:
                    if val is not None:
                        policy[field] = val

        if policy['forbidden']:
            return HttpResponseForbidden('<h1>HTTP 401 Forbidden</h1>')

        isSecure = requestIsSecure(request)
        if policy['sslRequired'] and not isSecure:
            return self._redirect(request, policy['sslRequired'])

        if isSecure and not policy['sslRequired'] and settings.GEOCAM_UTIL_SECURITY_TURN_OFF_SSL_WHEN_NOT_REQUIRED:
            return self._redirect(request, policy['sslRequired'])

        if policy['loginRequired']:
            authenticated = False

            for authType in ('django',) + tuple(policy['acceptAuthTypes']):
                if getattr(self, '_%sAuthenticate' % authType)(request):
                    authenticated = True
                    #print >>sys.stderr, 'authenticated via %s' % authType
                    break

            if not authenticated:
                return getattr(self, '_%sChallenge' % policy['challenge'])(request)

        return None

    def process_response(self, request, response):
        '''
        Patch the response from contrib.auth.views.login to redirect
        back to http if needed.  Note "?protocol=http" added in
        _djangoChallenge().
        '''
        if not settings.GEOCAM_UTIL_SECURITY_ENABLED:
            return response

        if isinstance(response, HttpResponseRedirect) and request.method == "POST":
            try:
                redirectTo = request.REQUEST.get('next', None)
            except:  # pylint: disable=W0702
                # probably badly formed request content -- log error and don't worry about it
                errClass, errObject, errTB = sys.exc_info()[:3]
                traceback.print_tb(errTB)
                print >> sys.stderr, '%s.%s: %s' % (errClass.__module__,
                                                    errClass.__name__,
                                                    str(errObject))
                return response
            print >> sys.stderr, 'redirectTo:', redirectTo
            print >> sys.stderr, 'next:', request.GET.get('next')
            if (redirectTo and redirectTo.endswith('?protocol=http')):
                initUrl = response['Location']
                url = request.build_absolute_uri(initUrl)
                url = re.sub(r'^https:', 'http:', url)
                url = re.sub(r'\?protocol=http$', '', url)
                response['Location'] = url
                print >> sys.stderr, 'process_response: redirectTo=%s initUrl=%s url=%s' % (redirectTo, initUrl, url)
        return response

    def _redirect(self, request, secure):
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError(
                """Django can't perform a SSL redirect while maintaining POST data.
                Please structure your views so that redirects only occur during GETs.""")

        protocol = secure and "https" or "http"

        newurl = "%s://%s%s" % (protocol, get_host(request), request.get_full_path())
        return HttpResponsePermanentRedirect(newurl)
