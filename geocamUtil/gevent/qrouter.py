# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
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
        for subscriberId, (topicPattern, q) in self._subs.iteritems():
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
