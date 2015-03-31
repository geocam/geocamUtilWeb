#!/usr/bin/env python
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

"""
A test file source to write files to be published by filePublisher.py.
"""

import logging
import os
import time


def dosys(cmd):
    print cmd
    os.system(cmd)


def testFileSource(opts, args):
    i = 0
    while 1:
        for f in args:
            _name, ext = os.path.splitext(f)
            dosys('cp %s %s/%06d%s' % (f, opts.output, i, ext))
            i += 1
            time.sleep(opts.period)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog OPTIONS <FILES>\n' + __doc__)
    parser.add_option('-o', '--output',
                      default='.',
                      help='Directory to write files to [%default]')
    parser.add_option('-p', '--period',
                      type='float', default=1.0,
                      help='Period between writing new files (seconds) [%default]')
    opts, args = parser.parse_args()
    if not args:
        parser.error('expected file arguments')

    logging.basicConfig(level=logging.DEBUG)

    testFileSource(opts, args)


if __name__ == '__main__':
    main()
