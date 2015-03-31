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

import itertools


class MultiSettings(object):
    """
    A settings container object built out of an ordered list of
    child settings objects.  When you request the value of an attribute,
    it returns the value found in the first child that defines that
    attribute.
    """
    def __init__(self, *sources):
        self._sources = sources

    def __getattr__(self, key):
        for src in self._sources:
            if hasattr(src, key):
                return getattr(src, key)
        raise AttributeError(key)

    def __dir__(self):
        return list(itertools.chain(*[dir(src) for src in self._sources]))

    # For Python < 2.6:
    __members__ = property(lambda self: self.__dir__())
