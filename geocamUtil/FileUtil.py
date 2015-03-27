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
