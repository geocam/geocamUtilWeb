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

"""
A wrapper module that tries multiple methods of importing JSON
support.  Recommended usage:

from geocamUtil import anyjson as json
"""

# tell pylint it's ok that we're importing wildcards
# pylint: disable=W0401

try:
    # user explicitly installed some version of simplejson module,
    # prefer their version
    from simplejson import *
except ImportError:
    try:
        # C-compiled simplejson included by default in Python 2.6+
        from json import *
    except ImportError:
        # backstop, Django ships with a (slower) pure-Python simplejson
        from django.utils.simplejson import *
