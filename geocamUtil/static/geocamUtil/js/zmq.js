// __BEGIN_LICENSE__
// Copyright (C) 2008-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__

/* url: url to connect to zmqProxy.py websockets server
   opts: can specify 'onopen' and 'onclose' handlers. can set autoReconnect to true. */
ZmqManager = function (url, opts) {
    this.url = url;
    this.opts = opts;

    this.socket = null;
    this.handlers = {};
    this.requestCounter = 0;
}

ZmqManager.prototype.start = function () {
    this.connect();
    if (this.opts.autoReconnect) {
        this.autoReconnect();
    }
};

ZmqManager.prototype.connect = function () {
    if (this.socket != null) {
        return;
    }
    this.socket = new WebSocket(this.url);
    this.socket.onmessage = function (self) {
        return function () {
            self.onmessage.apply(self, arguments);
        };
    }(this);
    this.socket.onopen = function (self) {
        return function () {
            self.onopen.apply(self);
        };
    }(this);
    this.socket.onclose = function (self) {
        return function () {
            self.onclose.apply(self);
        };
    }(this);
};

ZmqManager.prototype.autoReconnect = function () {
    this.connect();
    setTimeout(function (self) {
        return function () {
            self.autoReconnect.apply(self);
        }
    }(this), 2000);
};

ZmqManager.prototype.subscribeRaw = function (topic, handler) {
    this.handlers[topic] = handler;

    var request = {
        'jsonrpc': '2.0',
        'method': 'subscribe',
        'params': {
            'topic': topic
        },
        'id': this.requestCounter
    };
    this.requestCounter++;

    this.socket.send(JSON.stringify(request));
};

ZmqManager.prototype.subscribeJson = function (topic, handler) {
    function wrappedHandler(zmq, topic, body) {
        return handler(zmq, topic, JSON.parse(body));
    }
    this.subscribeRaw(topic, wrappedHandler);
};

ZmqManager.prototype.onmessage = function (msg) {
    var colonIndex = msg.data.search(':');
    var topicWithColon = msg.data.substr(0, colonIndex+1);
    var topic = msg.data.substr(0, colonIndex);
    var body = msg.data.substr(colonIndex+1);

    $.each(this.handlers, function (topicPrefix, handler) {
        if (topicWithColon.indexOf(topicPrefix) == 0) {
            handler(this, topic, body);
        }
    });
};

ZmqManager.prototype.onopen = function () {
    if (this.opts.onopen) {
        this.opts.onopen(this);
    }
};

ZmqManager.prototype.onclose = function () {
    if (this.opts.onclose) {
        this.opts.onclose(this);
    }
    this.socket = null;
};
