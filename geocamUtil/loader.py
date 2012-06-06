# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

"""
Utilities for loading Python classes and Django models by name. Modeled
in part on django.utils.importlib.
"""

def getModClass(name):
    """converts 'app_name.ModelName' to ['stuff.module', 'ClassName']"""
    try:
        dot = name.rindex('.')
    except ValueError:
        return name, ''
    return name[:dot], name[dot + 1:]


def getModelByName(qualifiedName):
    """
    converts 'module_name.ClassName' to a class object
    """
    appName, className = qualifiedName.split('.', 1)
    modelsName = '%s.models' % appName
    __import__(modelsName)
    mod = sys.modules[modelsName]
    return getattr(mod, className)
