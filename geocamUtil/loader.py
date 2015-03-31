# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

"""
Utilities for loading Python classes and Django models by name. Modeled
in part on django.utils.
"""

import sys

from django.db import models


def getModClass(name):
    """converts 'app_name.ModelName' to ['stuff.module', 'ClassName']"""
    try:
        dot = name.rindex('.')
    except ValueError:
        return name, ''
    return name[:dot], name[dot + 1:]


def getModelByName(qualifiedName):
    """
    converts 'appName.ModelName' to a class object
    """
    return models.get_model(*qualifiedName.split('.'))


class LazyGetModelByName(object):
    def __init__(self, qualifiedName):
        self.qualifiedName = qualifiedName
        self.result = None

    def get(self):
        if self.result is None:
            self.result = getModelByName(self.qualifiedName)
        return self.result


def getClassByName(qualifiedName):
    """
    converts 'moduleName.ClassName' to a class object
    """
    moduleName, className = qualifiedName.rsplit('.', 1)
    __import__(moduleName)
    mod = sys.modules[moduleName]
    return getattr(mod, className)


def getFormByName(qualifiedName):
    """
    converts 'module_name.forms.FormName' to a class object
    """
    appName, forms, className = qualifiedName.split('.', 2)
    formsName = '%s.%s' % (appName, forms)
    __import__(formsName)
    mod = sys.modules[formsName]
    return getattr(mod, className)
