#!/usr/bin/env python
# __BEGIN_LICENSE__
#Copyright © 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
#
#The xGDS platform is licensed under the Apache License, Version 2.0 
#(the "License"); you may not use this file except in compliance with the License. 
#You may obtain a copy of the License at 
#http://www.apache.org/licenses/LICENSE-2.0.
#
#Unless required by applicable law or agreed to in writing, software distributed 
#under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
#CONDITIONS OF ANY KIND, either express or implied. See the License for the 
#specific language governing permissions and limitations under the License.
# __END_LICENSE__

import logging

from zmq.eventloop import ioloop
ioloop.install()

from geocamUtil.zmqUtil.util import zmqLoop
from geocamUtil.zmqUtil.subscriber import ZmqSubscriber
from geocamUtil import anyjson as json


def handleMessagePretty(topic, obj):
    print topic
    print json.dumps(obj, sort_keys=True, indent=4)


def handleMessageSimple(topic, body):
    print '%s: %s' % (topic, body)


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <prefix>')
    parser.add_option('-p', '--pretty',
                      action='store_true', default=False,
                      help='Pretty-print JSON objects')
    ZmqSubscriber.addOptions(parser, 'zmqGrep')
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error('expected exactly 1 arg')
    logging.basicConfig(level=logging.DEBUG)

    # set up networking
    s = ZmqSubscriber(**ZmqSubscriber.getOptionValues(opts))
    s.start()

    # subscribe to the message we want
    topic = args[0]
    if opts.pretty:
        s.subscribeJson(topic, handleMessagePretty)
    else:
        s.subscribeRaw(topic, handleMessageSimple)

    zmqLoop()


if __name__ == '__main__':
    main()
