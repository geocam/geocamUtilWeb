#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import gevent
import gevent.monkey
gevent.monkey.patch_all(thread=False)
import zerorpc
from IPython.config.loader import Config
from IPython.frontend.terminal.embed import InteractiveShellEmbed
from IPython.lib.inputhook import inputhook_manager, stdin_ready

from geocamUtil.jsonConfig import loadConfig
from geocamUtil.zmq.zerorpcClientProxy import ClientProxy

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
        rpcPorts = self._ports.zerorpc
        for name, port in rpcPorts.iteritems():
            client = zerorpc.Client(port)
            # immediately set up simple proxy
            globals()[name] = ClientProxy(name, client)
            # set up background task to construct decorated proxy that replaces
            # simple proxy
            gevent.spawn(self.setDecoratedProxy, name, client)

        services = sorted(rpcPorts.keys())
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
    parser = optparse.OptionParser('usage: %prog')
    parser.add_option('-p', '--ports',
                      default='ports.json',
                      help='Path to ports config file [%default]')
    opts, args = parser.parse_args()
    if args:
        parser.error('expected no args')
    zclient(opts)


if __name__ == '__main__':
    main()
