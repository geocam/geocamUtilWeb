# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

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
