#!/usr/bin/env python

import os
import fcntl
import errno

import gevent
from gevent import socket
from gevent.queue import Queue


def copyFileToQueue(f, q):
    """
    Given a file *f* (probably the output pipe from a subprocess),
    asynchronously copy lines from the file into gevent Queue *q* until
    EOF is reached.
    """
    if isinstance(f, file):
        fd = f.fileno()
    else:
        fd = f

    # make file non-blocking
    flags = fcntl.fcntl(fd, fcntl.F_GETFL, 0)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

    buf = ''
    while 1:
        try:
            chunk = os.read(fd, 1024)
            if not chunk:
                break
        except OSError, ex:
            if ex[0] != errno.EAGAIN:
                raise
            chunk = None
        if chunk:
            buf += chunk
            while 1:
                ind = buf.find('\n')
                if ind == -1:
                    break
                else:
                    line = buf[:(ind + 1)]
                    q.put(line)
                    buf = buf[(ind + 1):]
        try:
            gevent.sleep(0.1)
            # socket.wait_read(fd)  # hangs. why?
        except socket.timeout:
            pass
    os.close(fd)
    q.put(StopIteration)


def queueFromFile(f):
    q = Queue()
    gevent.spawn(copyFileToQueue, f, q)
    return q
