# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import tempfile
import os

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

    #write to temporary pdf file
    tempInputFile = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    tempInputFile.seek(0)
    tempInputFile.write(data)
    tempInputFile.flush()

    outputFileName = tempInputFile.name.replace('.pdf', '.png')

    ret = os.system('convert -flatten %s %s > /dev/null' % (tempInputFile.name, outputFileName))

    os.remove(tempInputFile.name)

    if ret != 0 or os.path.isfile(outputFileName) == False:
        raise PdfConversionError('Error found while converting pdf')

    outputFile = open(outputFileName, 'r')
    outputFileData = outputFile.read()

    outputFile.close()
    os.remove(outputFileName)

    return outputFileData
