# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

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
