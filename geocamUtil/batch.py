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

from collections import deque


class BatchProcessor(object):
    def __init__(self, func, n):
        self.func = func
        self.n = n
        self.queue = deque()

    def add(self, elt):
        self.queue.append(elt)
        if len(self.queue) >= self.n:
            self.flush()

    def flush(self):
        self.func(self.queue)
        self.queue.clear()
