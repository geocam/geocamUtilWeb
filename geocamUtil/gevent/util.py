#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os
import fcntl
import errno
import re

import gevent
from gevent import socket
from gevent.queue import Queue


class LineParser(object):
    def __init__(self, handler, maxLineLength=None):
        self._buf = ''
        self._handler = handler
        self._maxLineLength = maxLineLength

    def write(self, text):
        self._buf += text
        while 1:
            m = re.search(r'\r\n|\n|\r', self._buf)
            ind = m.end() if m else None
            if (ind == None
                and self._maxLineLength is not None
                and len(self._buf) >= self._maxLineLength):
                ind = self._maxLineLength
            if ind == None:
                break
            else:
                line = self._buf[:ind]
                self._handler(line)
                self._buf = self._buf[ind:]

    def flush(self):
        if self._buf:
            self._handler(self._buf)
            self._buf = ''


END_OF_FILE = ('__EOF__',)


def safeRead(fd, chunkSize):
    try:
        chunk = os.read(fd, 1024)
    except OSError, ex:
        if ex[0] == errno.EAGAIN:
            return ''
        raise
    if not chunk:
        return END_OF_FILE
    return chunk


def setNonBlocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL, 0)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)


def copyFileToQueue(f, q, maxLineLength=None):
    """
    Given a file or file descriptor *f* (probably the output pipe from a
    subprocess), asynchronously copy lines from the file into gevent
    Queue *q* until EOF is reached. If *maxLineLength* is not None, break
    up long lines to have length at most that long.
    """
    if isinstance(f, file):
        fd = f.fileno()
    else:
        fd = f

    try:
        parser = LineParser(q.put, maxLineLength)

        setNonBlocking(fd)
        while 1:
            chunk = safeRead(fd, 1024)
            if chunk is END_OF_FILE:
                break
            if chunk:
                parser.write(chunk)
            try:
                gevent.sleep(0.1)
                # socket.wait_read(fd)  # hangs. why?
            except socket.timeout:
                pass

        parser.flush()

    finally:
        if isinstance(f, file):
            f.close()
        else:
            os.close(fd)
        q.put(StopIteration)


def queueFromFile(f, maxLineLength=None):
    q = Queue()
    gevent.spawn(copyFileToQueue, f, q, maxLineLength)
    return q
