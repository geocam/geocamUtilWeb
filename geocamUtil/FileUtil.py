# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os
import glob
import errno


class NoDataError(Exception):
    pass


def importModuleByName(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def getMiddleFileWithExtension(ext, path):
    allMatches = glob.glob('%s/*.%s' % (path, ext))
    allMatches = [x for x in allMatches
               if not x.startswith('thumbnail')]
    if not allMatches:
        raise NoDataError('no %s files in %s' % (ext, path))
    allMatches.sort()
    assert len(allMatches) > 0
    return allMatches[len(allMatches) // 2]


def mkdirP(d):
    try:
        os.makedirs(d)
    except OSError, err:
        if err.errno != errno.EEXIST:
            raise
