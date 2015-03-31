# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import time
try:
    from decorator import decorator
    HAVE_DECORATOR_MODULE = True
except ImportError:
    HAVE_DECORATOR_MODULE = False


if not HAVE_DECORATOR_MODULE:
    # roughly simulate the decorator module with functools
    from functools import wraps

    def decorator(metaFn):  # pylint: disable=E0102
        def resultingDecorator(fn):
            @wraps(fn)
            def outputFn(*args, **kwargs):
                return metaFn(fn, *args, **kwargs)
            return outputFn
        return resultingDecorator


class LogDecorator(object):
    """
    A decorator class for logging function calls. Example usage::

      import logging
      from geocamUtil.logDecorator import LogDecorator

      logging.basicConfig(level=logging.DEBUG)
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
        @decorator
        def resultFn(fn, *args, **kwargs):
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
        return resultFn
