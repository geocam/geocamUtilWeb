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

from geocamUtil import anyjson as json


def convertToDotDictRecurse(struct):
    if isinstance(struct, dict):
        for k, v in struct.iteritems():
            struct[k] = convertToDotDictRecurse(v)
        return DotDict(struct)
    elif isinstance(struct, list):
        return [convertToDotDictRecurse(elt) for elt in struct]
    else:
        return struct


class DotDict(dict):
    # At the moment this object exists pretty much solely to let you
    # get and set elements in its __dict__ dictionary via dotted
    # notation.  Someday it could do more.

    # these are fields that must not be defined to avoid causing problems
    # with Django
    _badFields = ('prepare_database_save',)

    def copy(self):
        return DotDict(self)

    def __repr__(self):
        return json.dumps(self, sort_keys=True, indent=4)

    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise AttributeError(attr)  # avoids breaking copy.deepcopy
        if attr in self._badFields:
            raise KeyError(attr)
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
