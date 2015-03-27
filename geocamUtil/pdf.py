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

    if ret != 0 or os.path.isfile(outputFileName) is False:
        raise PdfConversionError('Error found while converting pdf')

    outputFile = open(outputFileName, 'r')
    outputFileData = outputFile.read()

    outputFile.close()
    os.remove(outputFileName)

    return outputFileData
