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
