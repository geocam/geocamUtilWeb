# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
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

    def copy(self):
        return DotDict(self)

    def __repr__(self):
        return json.dumps(self, sort_keys=True, indent=4)

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            return super(DotDict,self).__getattribute__(attr)


    def __setattr__(self, name, value):
        if name in dir(self):
            raise AttributeError("Cannot shadow built-in dict attribute: %s" %
                                 name)
        else:
            self[name] = value


    def __delattr__(self, name):
        if name in dir(self):
            super(DotDict, self).__delattr__(name)
        else:
            del self[name]
