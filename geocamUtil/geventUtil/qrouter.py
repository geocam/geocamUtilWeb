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

from fnmatch import fnmatch

from gevent.queue import Queue


class QueueRouter(object):
    def __init__(self):
        self._subs = {}

    def subscribe(self, topicPattern):
        q = Queue()
        self._subs[id(q)] = (topicPattern, q)
        return q

    def unsubscribe(self, q):
        if isinstance(q, int):
            qid = q
        else:
            qid = id(q)
        del self._subs[qid]

    def publish(self, topic, msg):
        for _subscriberId, (topicPattern, q) in self._subs.iteritems():
            if fnmatch(topic, topicPattern):
                q.put((topic, msg))

    def hasSubscribers(self):
        return self._subs != {}

    def getQueueInfo(self, q):
        if isinstance(q, int):
            qid = q
        else:
            qid = id(q)
        return self._subs[qid]
