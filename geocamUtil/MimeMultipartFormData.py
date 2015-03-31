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

# pylint: disable=R0924

import random
import StringIO


class MimeMultipartFormData(object):
    def __init__(self, **kwargs):
        self._boundary = '%032x' % random.getrandbits(128)
        self._fields = kwargs.get('fields', {})
        self._files = kwargs.get('files', [])

    def __getitem__(self, k):
        return self._fields[k]

    def __setitem__(self, k, v):
        self._fields[k] = v

    def getHeaders(self):
        return {'Content-Type': 'multipart/form-data; boundary=%s' % self._boundary}

    def addFile(self, name, filename, data, contentType='text/plain'):
        self._files.append((name, filename, data, contentType))

    def writePostData(self, stream):
        for k, v in self._fields.iteritems():
            stream.write('\r\n--%s\r\n' % self._boundary)
            stream.write('Content-Disposition: form-data; name="%s"\r\n' % k)
            stream.write('Content-Type: text/plain\r\n')
            stream.write('\r\n')
            stream.write(v)
        for name, filename, data, contentType in self._files:
            stream.write('\r\n--%s\r\n' % self._boundary)
            stream.write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
                         % (name, filename))
            stream.write('Content-Type: %s\r\n' % contentType)
            stream.write('\r\n')
            stream.write(data)
        stream.write('\r\n--%s--\r\n' % self._boundary)

    def getPostData(self):
        stream = StringIO.StringIO()
        self.writePostData(stream)
        return stream.getvalue()
