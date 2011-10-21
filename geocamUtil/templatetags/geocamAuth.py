# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import re

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from geocamUtil.middleware.SecurityMiddleware import requestIsSecure
from geocamUtil import settings

register = template.Library()


class PasswordUrlNode(template.Node):
    def __init__(self, urlName):
        super(PasswordUrlNode, self).__init__()
        self.urlName = urlName

    def render(self, context):
        url = reverse(self.urlName)
        request = context['request']
        if (settings.GEOCAM_UTIL_SECURITY_ENABLED
            and not requestIsSecure(request)
            and settings.GEOCAM_UTIL_SECURITY_REQUIRE_ENCRYPTED_PASSWORDS):
            secureUrl = re.sub('^http:', 'https:', request.build_absolute_uri(url)) + '?protocol=http'
            return secureUrl
        else:
            return url

    def __repr__(self):
        return "<PasswordUrlNode urlName=%s>" % self.urlName


@register.tag
def password_url(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError('%s tag requires exactly 1 argument' % bits[0])
    return PasswordUrlNode(bits[1])
