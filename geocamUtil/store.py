# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import os
import re
import urllib
try:
    import cPickle as pickle
except ImportError:
    import pickle
import zlib
from collections import deque, MutableMapping
import logging
import json

loggerG = logging.getLogger('geocamUtil.store')


def encodeVal(val):
    return zlib.compress(pickle.dumps(val, pickle.HIGHEST_PROTOCOL), 9)


def decodeVal(s):
    return pickle.loads(zlib.decompress(s))


class FileStore(MutableMapping):
    """
    Key/value store that uses the dict API. Keys must be strings. Values
    may have arbitrary types but must be pickle-compatible.

    Persistently stores key/value pairs on disk, one file per pair. The
    filename is the key (with some escaping) and the file contents are
    the pickled and compressed value.

    The directory argument to the constructor specifies what directory the
    files go in. The directory structure within that dir is flat, so a
    large number of keys means a large number of files in the same
    directory.  This should perform ok under Mac OS HFS+ and Linux ext4
    (B-tree indexed directories) but might not under other file systems.
    """
    def __init__(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def getPath(self, key):
        return os.path.join(self.directory, urllib.quote_plus(key)) + '.p.gz'

    def __getitem__(self, key):
        path = self.getPath(key)
        exists = os.path.exists(path)
        try:
            data = file(path, 'rb').read()
        except (IOError, OSError):
            raise KeyError(key)
        logging.debug('FileStore read: key=%s path=%s exists=%s len(data)=%s',
                      key, path, exists, len(data))
        return decodeVal(data)

    def __setitem__(self, key, val):
        data = encodeVal(val)
        path = self.getPath(key)
        logging.debug('FileStore write: key=%s path=%s len(data)=%s',
                      key, path, len(data))
        pathTmp = '%s.part' % path
        try:
            file(pathTmp, 'wb').write(data)
            os.rename(pathTmp, path)
        except (IOError, OSError):
            raise KeyError(key)

    def __delitem__(self, key):
        try:
            os.remove(self.getPath(key))
        except (IOError, OSError):
            raise KeyError(key)

    def __contains__(self, key):
        return os.path.exists(self.getPath(key))

    def __len__(self):
        return len(os.path.listdir(self.directory))

    def __iter__(self):
        for name in os.listdir(self.directory):
            yield urllib.unquote_plus(re.sub(r'\.p\.gz$', '', name))

    def sync(self):
        # entries are sync'd as they are added, nothing to do
        pass


class CacheInfo(object):
    """
    An internal data structure used by LruCacheStore.
    """
    def __init__(self):
        self.dirty = False
        self.refCount = 0


class LruCacheStore(MutableMapping):
    """
    Key/value store that uses the dict API. Keys must be strings. Values
    may have arbitrary types but must be pickle-compatible.

    Key/value pairs are preferentially stored in the cache. When the
    size of the cache exceeds maxEntries, the least recently used cache
    entries are flushed to the store and evicted. sync() flushes the
    entire cache to the store.

    The LRUCacheStore has no way to tell when you modify the internal
    structure of a value already in the cache, so to ensure consistency,
    every time you modify a value you must either call
    store.markWrite(key) or set store[key] = value again.
    """
    def __init__(self, store, maxEntries, cache=None, flushCallback=None):
        self.store = store
        self.maxEntries = maxEntries
        if cache is None:
            cache = dict()
        self.cache = cache
        self.flushCallback = flushCallback
        self.cacheInfo = {}
        self.queue = deque()

    def markUsed(self, key, isWrite):
        cacheInfo = self.cacheInfo.setdefault(key, CacheInfo())
        cacheInfo.refCount += 1
        self.queue.append(key)
        if isWrite:
            cacheInfo.dirty = True
        if len(self.queue) > self.maxEntries * 4:
            self.purgeQueue()

    def markWrite(self, key):
        self.markUsed(key, True)

    def markRead(self, key):
        self.markUsed(key, False)

    def purgeQueue(self):
        """
        The queue logs the order of when keys were accessed. To
        calculate the least recently used key, we only care about the
        most recent (rightmost) access entry for each key.  purgeQueue()
        rebuilds the queue eliminating other access entries to reduce
        the queue size.
        """
        for _i in xrange(0, len(self.queue)):
            key = self.queue.popleft()
            cacheInfo = self.cacheInfo[key]
            if cacheInfo.refCount == 1:
                self.queue.append(key)
            else:
                cacheInfo.refCount -= 1

    def flushEntry(self, key):
        loggerG.debug('flushEntry %s', key)
        cacheInfo = self.cacheInfo[key]
        if cacheInfo.dirty:
            val = self.cache[key]
            self.store[key] = val
            if self.flushCallback is not None:
                self.flushCallback(key, val)
            cacheInfo.dirty = False

    def evictEntry(self, key):
        loggerG.debug('evictEntry %s', key)
        self.flushEntry(key)
        del self.cache[key]
        del self.cacheInfo[key]

    def evictLru(self):
        while len(self.cache) >= self.maxEntries:
            key = self.queue.popleft()
            cacheInfo = self.cacheInfo.get(key, None)
            if cacheInfo:
                if cacheInfo.refCount == 1:
                    self.evictEntry(key)
                else:
                    cacheInfo.refCount -= 1

    def sync(self):
        for key, cacheInfo in self.cacheInfo.iteritems():
            if cacheInfo.dirty:
                self.flushEntry(key)

    def __getitem__(self, key):
        if key in self.cache:
            self.markRead(key)
            return self.cache[key]
        else:
            # hm... add to cache?
            return self.store[key]

    def __setitem__(self, key, val):
        if key not in self.cache and len(self.cache) >= self.maxEntries:
            self.evictLru()
        self.cache[key] = val
        self.markWrite(key)

    def __delitem__(self, key):
        foundKey = False
        if key in self.cache:
            del self.cache[key]
            foundKey = True
        if key in self.store:
            del self.store[key]
            foundKey = True
        if not foundKey:
            raise KeyError(key)

    def __iter__(self):
        for key in set(self.cache.keys()).union(set(self.store.keys())):
            yield key

    def __contains__(self, key):
        return key in self.cache or key in self.store

    def __len__(self):
        return len(self.keys())

    def __del__(self):
        self.sync()


class JsonStore(dict):
    """
    Key/value store that uses the dict API. Keys must be strings. Values
    may have arbitrary types but must be json-compatible.

    Persistently stores key/value pairs in a single JSON file on disk.

    The path argument to the constructor specifies where to write the file.
    """
    def __init__(self, path, initialValues=None):
        self.path = path
        if os.path.exists(path):
            self.update(json.load(open(path, 'r')))
        else:
            if initialValues is None:
                pass
            else:
                if callable(initialValues):
                    self.update(initialValues())
                else:
                    self.update(initialValues)
        super(JsonStore, self).__init__()

    def sync(self):
        parentDir = os.path.dirname(self.path)
        if not os.path.exists(parentDir):
            os.makedirs(parentDir)
        json.dump(self, open(self.path, 'w'), indent=4, sort_keys=True)
