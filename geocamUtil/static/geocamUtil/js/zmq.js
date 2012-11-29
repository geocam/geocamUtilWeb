// __BEGIN_LICENSE__
// Copyright (C) 2008-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__

/* url: url to connect to zmqProxy.py websockets server
   opts: can specify 'onopen' and 'onclose' handlers.
         can set autoReconnect to true. */
ZmqManager = function(url, opts) {
    this.url = url;
    this.opts = opts;

    this.socket = null;
    this.handlers = {};
    this.requestCounter = 0;
};

ZmqManager.prototype.start = function() {
    this.connect();
    if (this.opts.autoReconnect) {
        this.autoReconnect();
    }
};

ZmqManager.prototype.connect = function() {
    if (this.socket != null) {
        return;
    }
    this.socket = new WebSocket(this.url);
    this.socket.onmessage = function(self) {
        return function() {
            self.onmessage.apply(self, arguments);
        };
    }(this);
    this.socket.onopen = function(self) {
        return function() {
            self.onopen.apply(self);
        };
    }(this);
    this.socket.onclose = function(self) {
        return function() {
            self.onclose.apply(self);
        };
    }(this);
};

ZmqManager.prototype.autoReconnect = function() {
    this.connect();
    setTimeout(function(self) {
        return function() {
            self.autoReconnect.apply(self);
        }
    }(this), 2000);
};

ZmqManager.prototype.sendRequest = function(method, params) {
    var request = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': this.requestCounter
    };
    this.requestCounter++;

    this.socket.send(JSON.stringify(request));
};

ZmqManager.prototype.subscribeRaw = function(topicPrefix, handler) {
    var handlerId = this.requestCounter;
    this.handlers[handlerId] = {
        handlerId: handlerId,
        topicPrefix: topicPrefix,
        handler: handler
    };
    this.sendRequest('subscribe',
                     {
                         'topicPrefix': topicPrefix
                     });
    return handlerId;
};

ZmqManager.prototype.subscribeJson = function(topicPrefix, handler) {
    function wrappedHandler(zmq, topicPrefix, body) {
        return handler(zmq, topicPrefix, JSON.parse(body));
    }
    return this.subscribeRaw(topicPrefix, wrappedHandler);
};

ZmqManager.prototype.subscribeDjango = function(topicPrefix, handler) {
    function wrappedHandler(zmq, topicPrefix, body) {
        return handler(zmq, topicPrefix, JSON.parse(body).data.fields);
    }
    return this.subscribeRaw(topicPrefix, wrappedHandler);
};

ZmqManager.prototype.unsubscribe = function(handlerId) {
    var handlerInfo = this.handlers[handlerId];
    handlerInfo.unsubscribeRequested = true;
    this.unsubscribeIfNeeded(handlerId);
};

ZmqManager.prototype.unsubscribeIfNeeded = function(handlerId) {
    var handlerInfo = this.handlers[handlerId];
    if (handlerInfo.serverHandlerId != undefined &&
        handlerInfo.unsubscribeRequested) {
        this.sendRequest('unsubscribe',
                         {
                             'handlerId': handlerInfo.serverHandlerId
                         });
        delete this.handlers[handlerId];
    }
};

ZmqManager.prototype.handleResponse = function(topic, body) {
    // This response handler is simplified because we only need to watch
    // for responses to 'subscribe' requests and we chose the jsonrpc
    // request id to match the handlerId.
    var obj = JSON.parse(body);
    if (obj.id != undefined) {
        var handlerId = obj.id;
        var handlerInfo = this.handlers[handlerId];
        if (handlerInfo != undefined) {
            // Looks like a subscribe response
            if (obj.result == undefined) {
                // Error handling would be nice but not clear what we
                // should do.
            } else {
                handlerInfo.serverHandlerId = obj.result;
                // Check if the client-side code already tried to
                // unsubscribe before we received the subscribe reply.
                this.unsubscribeIfNeeded(handlerId);
            }
        }
    }
};

ZmqManager.prototype.onmessage = function(msg) {
    var colonIndex = msg.data.search(':');
    var topicWithColon = msg.data.substr(0, colonIndex + 1);
    var topic = msg.data.substr(0, colonIndex);
    var body = msg.data.substr(colonIndex + 1);

    // special case: handle jsonrpc response
    if (topic == 'zmqProxy.response') {
        this.handleResponse(topic, body);
    }

    // otherwise handle subscriptions
    $.each(this.handlers, function(handlerId, handlerInfo) {
        if (topicWithColon.indexOf(handlerInfo.topicPrefix) == 0) {
            handlerInfo.handler(this, topic, body);
        }
    });
};

ZmqManager.prototype.onopen = function() {
    if (this.opts.onopen) {
        this.opts.onopen(this);
    }
};

ZmqManager.prototype.onclose = function() {
    if (this.opts.onclose) {
        this.opts.onclose(this);
    }
    this.socket = null;
    this.handlers = {};
};
