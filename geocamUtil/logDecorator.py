# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import time
from functools import wraps


class LogDecorator(object):
    """
    A decorator class for logging function calls. Example usage::

      import logging
      from geocamUtil.logDecorator import LogDecorator

      logger = logging.getLogger('foo')
      log = LogDecorator(logger)

      @log()
      def bar(x):
          return x * x

      bar(2)

    Should log::

      DEBUG:foo:BEGIN bar(2)
      DEBUG:foo:END   bar result=4 elapsed=0.0001
    """

    def __init__(self, logger):
        self._logger = logger

    def __call__(self, no_result=False):
        def decorator(fn):
            @wraps(fn)
            def wrapped(*args, **kwargs):
                allArgs = tuple([repr(a) for a in args[1:]] +
                                ['%s=%s' % (k, repr(v))
                                 for k, v in kwargs.iteritems()])
                allArgsStr = '(%s)' % (', '.join(allArgs))
                self._logger.debug('BEGIN %s%s', fn.__name__, allArgsStr)
                startTime = time.time()
                try:
                    result = fn(*args, **kwargs)
                except Exception, ex:
                    endTime = time.time()
                    self._logger.debug('END %s result=%s elapsed=%s',
                                       fn.__name__,
                                       repr(ex),
                                       endTime - startTime)
                    raise
                endTime = time.time()
                if no_result:
                    resultStr = ''
                else:
                    resultStr = ' result=%s' % repr(result)
                self._logger.debug('END   %s%s elapsed=%s',
                                   fn.__name__,
                                   resultStr,
                                   endTime - startTime)
                return result
            return wrapped
        return decorator
