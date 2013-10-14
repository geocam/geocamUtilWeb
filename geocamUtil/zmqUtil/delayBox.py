# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from zmq.eventloop import ioloop


class DelayBox(object):
    """
    DelayBox helps you intelligently delay things like cache flushing so as
    to minimize redundant effort.

    Example usage:

    delayBox = DelayBox(foo, maxDelaySeconds=5, numBuckets=50)
    delayBox.start()
    delayBox.addJob(1)
    delayBox.addJob(1)
    delayBox.addJob(2)
    delayBox.addJob(2)
    delayBox.stop()

    When jobCallback=foo, delayBox.addJob(1) is setting up a delayed
    call to foo(1) -- the delay is at most maxDelaySeconds. However, if
    you call addJob(1) multiple times before the DelayBox gets around to
    calling foo(1), those multiple addJob(1) calls are collapsed into
    one delayed call to foo(1).

    To improve resource utilization (e.g. disk I/O), the DelayBox
    implementation tries not to bunch up execution of all jobs in big
    bursts. It does this by dividing jobs up into buckets. More buckets
    should spread out jobs more evenly but also means the DelayBox wakes
    up more often.

    The argument type passed to addJob must be suitable for use as a
    Python dict key (e.g. string, int, tuple -- but no mutable types).
    """

    def __init__(self, jobCallback, maxDelaySeconds=5, numBuckets=50):
        self.updateInterval = float(maxDelaySeconds) / numBuckets
        assert self.updateInterval != 0
        self.numBuckets = numBuckets
        self.jobCallback = jobCallback

        self.buckets = []
        for _i in xrange(numBuckets):
            self.buckets.append({})
        self.counter = 0
        self.event = None
        self.timer = None

    def addJob(self, arg):
        bucketIndex = hash(arg) % self.numBuckets
        self.buckets[bucketIndex][arg] = True

    def intervalHandler(self):
        self.flushBucket(self.buckets[self.counter])
        self.counter = (self.counter + 1) % self.numBuckets

    def flushBucket(self, bucket):
        for arg in bucket:
            self.jobCallback(arg)
        bucket.clear()

    def sync(self):
        for bucket in self.buckets:
            self.flushBucket(bucket)

    def start(self):
        self.timer = ioloop.PeriodicCallback(self.intervalHandler,
                                             self.updateInterval * 1000)
        self.timer.start()

    def stop(self):
        self.sync()
        self.timer.stop()
        self.timer = None
