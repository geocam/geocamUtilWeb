# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

CLASS_TEMPLATE = """
class %(decoratedName)s(%(parentName)s):
"""

FUNC_TEMPLATE = """
    def %(name)s(self, %(signature)s):
        %(docstring)s
        return self._client.%(name)s(%(signature)s)
"""


def firstCaps(s):
    if s:
        return s[0].upper() + s[1:]
    else:
        return s


class ClientProxy(object):
    def __init__(self, name, client):
        self._name = name
        self._client = client

    def __getattr__(self, name):
        # don't intercept requests for special attributes
        if name.startswith('__'):
            raise AttributeError(name)
        return getattr(self._client, name)

    @classmethod
    def makeDecoratedProxy(cls, name, client):
        try:
            meta = client._zerorpc_inspect()
        except:  # pylint: disable=W0702
            #print ('could not inspect methods for service %s, may not be running'
            #       % self._name)
            return None
        decoratedName = '%sClient' % firstCaps(name)
        src = (CLASS_TEMPLATE
               % {'decoratedName': decoratedName,
                  'parentName': cls.__name__})

        methods = meta['methods']
        for name, info in methods.iteritems():
            argNames = [arg['name'] for arg in info['args']]
            signature = ', '.join(argNames[1:])
            docstring = repr(info.get('doc', '<unknown>'))
            src += (FUNC_TEMPLATE
                    % {'name': name,
                       'signature': signature,
                       'docstring': docstring})
        code = compile(src, '<string>', 'single')
        evaldict = {'__name__': 'geocamUtil.zmq.zerorpcClientProxy',
                    'ClientProxy': ClientProxy}
        exec code in evaldict  # pylint: disable=W0122
        return evaldict[decoratedName]
