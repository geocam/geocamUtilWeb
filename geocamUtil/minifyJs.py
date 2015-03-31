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

import os
import logging


def minifyJsExecute(dst, srcPairs):
    # don't import unless minifyJsExecute is actually called (usually won't be)
    from slimit import minify

    dstDir = os.path.dirname(dst)
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)

    dstPart = '%s.part' % dst
    out = file(dstPart, 'w')
    for src, doMinify in srcPairs:
        text = file(src, 'r').read()
        if doMinify:
            logging.debug('adding %s (with minify)', src)
            # mangling sometimes messes up exported identifiers, oh well
            out.write(minify(text, mangle=False))
        else:
            logging.debug('adding %s (without minify)', src)
            out.write(text)
        out.write(';')
    out.close()
    os.rename(dstPart, dst)


def minifyJs(builder, dst, srcPairs):
    srcs = [pr[0] for pr in srcPairs]
    builder.applyRule(dst, srcs, lambda: minifyJsExecute(dst, srcPairs))
