# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

class PdfConversionError(Exception):
    pass


def convertPdf(data,
               imageWidth=1000,
               dstContentType='image/png',
               fileName='dummyFileName',
               pageNumber=None):
    """
    Pass in the raw binary PDF data. Returns the raw binary image data
    result after rasterization.
    """
    raise NotImplementedError()
