# __BEGIN_LICENSE__
# Copyright (c) 2015, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
# __END_LICENSE__

"""
Utilities for converting models to json
"""
import json
from django.forms import model_to_dict


def modelToDict(model, fields=None, exclude=None):
    return model_to_dict(model, fields, exclude)


def dictToJson(dict, encoder=None):
    return json.dumps(dict, cls=encoder)


def modelToJson(model, encoder=None):
    theDict = model_to_dict(model)
    return json.dumps(theDict, cls=encoder)


def modelsToJson(models, encoder=None):
    result = []
    for model in models:
        result.append(modelToJson(model, encoder))
    return result
