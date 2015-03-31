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

import sys
import traceback


class LogErrorsMiddleware(object):
    """Makes exceptions thrown within the django app print debug information
    to stderr so that it shows up in the Apache error log."""
    def process_exception(self, req, exception):
        errClass, errObject, errTB = sys.exc_info()[:3]
        traceback.print_tb(errTB)
        print >> sys.stderr, '%s.%s: %s' % (errClass.__module__,
                                            errClass.__name__,
                                            str(errObject))
