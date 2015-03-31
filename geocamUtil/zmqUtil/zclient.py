#!/usr/bin/env python
# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

# pylint: disable=E0611,E1101

import sys

import gevent
import gevent.monkey
gevent.monkey.patch_all(thread=False)
import zerorpc
from IPython.config.loader import Config
from IPython.terminal.embed import InteractiveShellEmbed
from IPython.lib.inputhook import inputhook_manager, stdin_ready
try:
    from django.conf import settings
except ImportError:
    settings = object()

from geocamUtil.jsonConfig import loadConfig
from geocamUtil.zmqUtil.zerorpcClientProxy import ClientProxy

INTRO_TEMPLATE = """
Welcome to zclient.

This is an IPython shell with zerorpc clients for services from the
ports.json file bound to variables in the shell environment. The
following services are defined:

%(services)s

To call service 'foo' method 'bar', type 'foo.bar()'. For more
information, type 'help(foo)' or 'help(foo.bar)'. Note that the help()
functions only work if the service in question is available when zclient
starts.
"""


def inputhook_gevent():
    try:
        while not stdin_ready():
            gevent.sleep(0.05)
    except KeyboardInterrupt:
        pass
    return 0


class Shell(object):
    def __init__(self, opts):
        self._opts = opts
        self._ports = loadConfig(self._opts.ports)

    def setDecoratedProxy(self, name, client):
        proxyClass = ClientProxy.makeDecoratedProxy(name, client)
        if proxyClass:
            globals()[name] = proxyClass(name, client)

    def run(self):
        # tell ipython to use gevent as the mainloop
        inputhook_manager.set_inputhook(inputhook_gevent)

        # initialize clients
        for name, info in self._ports.iteritems():
            port = info.get('rpc')
            if port is None:
                continue
            heartbeat = info.get('rpcHeartbeat', 5)
            timeout = info.get('rpcTimeout', 99999)
            client = zerorpc.Client(port,
                                    heartbeat=heartbeat,
                                    timeout=timeout)
            # immediately set up simple proxy
            globals()[name] = ClientProxy(name, client)
            if not self._opts.command:
                # set up background task to construct decorated proxy that replaces
                # simple proxy
                gevent.spawn(self.setDecoratedProxy, name, client)

        if self._opts.command:
            exec(self._opts.command)
            gevent.sleep(0.1)
            sys.exit(0)

        services = sorted(self._ports.keys())
        servicesStr = '\n'.join(['  %s' % svc for svc in services])
        intro = INTRO_TEMPLATE % {'services': servicesStr}
        ipshell = InteractiveShellEmbed(config=Config(),
                                        banner1=intro)
        ipshell()


def zclient(opts):
    shell = Shell(opts)
    shell.run()


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog OPTIONS')
    parser.add_option('-p', '--ports',
                      default=getattr(settings, 'GEOCAM_UTIL_ZMQ_PORTS_PATH', 'ports.json'),
                      help='Path to ports config file [%default]')
    parser.add_option('-c', '--command',
                      help='If specified, eval command and exit')
    opts, args = parser.parse_args()
    if args:
        parser.error('expected no args')
    zclient(opts)


if __name__ == '__main__':
    main()
