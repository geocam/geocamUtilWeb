#__BEGIN_LICENSE__
# Copyright (c) 2015, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The xGDS platform is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#__END_LICENSE__

import sys
from fnmatch import fnmatch

from django import template
from django.utils.encoding import smart_str
from django.core.urlresolvers import resolve, Resolver404, get_script_prefix


register = template.Library()


class NavNode(template.Node):
    def __init__(self, item=None, var_name=None):
        self.item = item
        self.var_name = var_name or 'nav'

    def render(self, context):
        # If the nav variable is already set (to a non-empty value), don't do
        # anything.
        if context.get(self.var_name):
            return ''
        # If self.item was blank, just set the nav variable to the context
        # (useful to put the nav in a higher context stack)
        if not self.item:
            context[self.var_name] = {}
            return ''
        item = self.item.resolve(context)
        item = item and smart_str(item)
        if not item:
            return ''
        value = True
        for part in reversed(item.split('.')):
            new_item = {}
            new_item[part] = value
            value = new_item
        # The nav variable could have been set (as an empty dict) on a higher
        # context stack. Try getting it from the context, otherwise set it to
        # the current context stack.
        navVal = context.get(self.var_name)
        if not isinstance(navVal, dict):
            navVal = {}
            context[self.var_name] = navVal
        navVal.update(new_item)
        return ''

    def __repr__(self):
        return "<Nav node>"


@register.tag
def nav(parser, token):
    """
    Handles navigation item selection.

    Example usage::

        {# Set up the variable for use across context-stacking tags #}
        {% nav %} or {% nav for mynav %}

        {# Set the context so {{ nav.home }} (or {{ mynav.home }}) is True #}
        {% nav "home" %} or {% nav "home" for mynav %}

    The most basic (and common) use of the tag is to call ``{% nav [item] %}``,
    where ``[item]`` is the item you want to check is selected.

    By default, this tag creates a ``nav`` context variable. To use an
    alternate context variable name, call ``{% nav [item] for [var_name] %}``.

    To use this tag across ``{% block %}`` tags (or other context-stacking
    template tags such as ``{% for %}``), call the tag without specifying an
    item.

    Your HTML navigation template should look something like::

        {% block nav %}
        <ul class="nav">
            <li{% if nav.home %} class="selected"{% endif %}><a href="/">Home</a></li>
            <li{% if nav.about %} class="selected"{% endif %}><a href="/about/">About</a></li>
        </ul>
        {% endblock %}

    To override this in a child template, you'd do::

        {% include "base.html" %}
        {% load nav %}

        {% block nav %}
        {% nav "about" %}
        {{ block.super }}
        {% endblock %}

    This works for multiple levels of template inheritance, due to the fact
    that the tag only does anything if the ``nav`` context variable does not
    exist. So only the first ``{% nav %}`` call found will ever be processed.

    To create a sub-menu you can check against, simply dot-separate the item::

        {% nav "about_menu.info" %}

    This will be pass for both ``{% if nav.about_menu %}`` and
    ``{% if nav.about_menu.info %}``.
    """
    bits = token.split_contents()
    if len(bits) > 2:
        var_name = bits.pop()
        for_bit = bits.pop()
        if for_bit != 'for' or len(bits) > 2:
            raise template.TemplateSyntaxError('Unexpected format for %s tag' %
                                               bits[0])
    else:
        var_name = 'nav'
    if len(bits) > 1:
        item = parser.compile_filter(bits[1])
    else:
        item = None
    return NavNode(item, var_name)


class CurrentNavNode(template.Node):
    def __init__(self, urlGlobs):  # pylint: disable=W0231
        self.urlGlobs = urlGlobs

    def render(self, context):
        requestPath = context['request'].path
        if len(get_script_prefix()) > 0:
            requestPath = requestPath[len(get_script_prefix()) - 1:]

        try:
            resolverMatch = resolve(requestPath)
        except Resolver404:
            print >> sys.stderr, 'CurrentNavNode: failed to resolve path %s' % requestPath
            return ''

        for pat in self.urlGlobs:
            if fnmatch(resolverMatch.url_name, pat):
                return ' active'
        return ''

    def __repr__(self):
        return "<CurrentNav node urlGlobs=%s>" % self.urlGlobs


@register.tag
def currentnav(parser, token):
    """
    The currentnav tag helps you highlight the current tab in a
    navigation bar based on Django's URL resolution system.  You specify
    some glob-style url name patterns:

    {% currentnav foo* blah %}

    If the current request resolves to a Django URL pattern whose name
    is (for example) 'foobar' or 'blah', then the tag renders the text
    ' class="currentnav"'. Otherwise the tag renders an empty string. At
    least one url name pattern must be specified.

    Example usage:

    # urls.py

    urlpatterns += patterns(,
      (r'^/home/$', view_home_method, {}, 'home_name'),
      (r'^/maps/$', view_maps_method, {}, 'maps_name'),
      (r'^/street_map/$', view_street_map_method, {}, 'street_map_name'),
      (r'^/weather_radar/$', view_weather_radar_method, {}, 'weather_radar_name'),
    )

    # mynavbar.html

    {% load nav %}

    <ul>
      <li {% currentnav home_name %}><a href="/home/">Home</a></li>
      <li {% currentnav *map*_name weather_radar_name %}><a href="/maps/">Maps</a></li>
    </ul>

    # views.py

    return render_to_response('my.html',
                              # the template context must include the request object
                              context_instance=RequestContext(request))

    # settings.py

    TEMPLATE_CONTEXT_PROCESSORS = (
       ...,
       # the template context must include the request object
       'django.core.context_processors.request',
    )

    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError('%s tag requires an argument' % bits[0])
    return CurrentNavNode(bits[1:])
