from geocamUtil import anyjson as json


class JsonRpc2Keys(object):
    KEY_JSONRPC = 'jsonrpc'
    KEY_METHOD = 'method'
    KEY_ID = 'id'
    KEY_PARAMS = 'params'
    KEY_RESULT = 'result'
    KEY_ERROR = 'error'
    KEY_ERROR_CODE = 'code'
    KEY_ERROR_MSG = 'message'


class JsonRpc2ComplianceException(Exception):
    def __init__(self, msg):
        super(JsonRpc2ComplianceException, self).__init__()
        self.msg = msg


class JsonRpc2Validator(object):
    def __init__(self):
        pass

    def validate(self, dataStr):
        try:
            data = json.loads(dataStr)
        except ValueError, valerr:
            print valerr
            raise JsonRpc2ComplianceException("Could not parse data into json object: %s" % str(valerr))

        # Check that data conforms to JSON-RPC v2.0
        if JsonRpc2Keys.KEY_JSONRPC not in data:
            raise JsonRpc2ComplianceException("%s missing from request" % JsonRpc2Keys.KEY_JSONRPC)
        if data[JsonRpc2Keys.KEY_JSONRPC] != '2.0':
            raise JsonRpc2ComplianceException("Data must be version 2.0. %s value is [%s]"
                                              % (JsonRpc2Keys.KEY_JSONRPC, data[JsonRpc2Keys.KEY_JSONRPC]))
# Can't validate ID since it's omission is considered a valid Notification
#        if JsonRpc2Keys.KEY_ID not in data:
#            raise JsonRpc2ComplianceException( "%s missing from data."%(JsonRpc2Keys.KEY_ID) )
        is_request = JsonRpc2Keys.KEY_METHOD in data
        is_resp = JsonRpc2Keys.KEY_RESULT in data or JsonRpc2Keys.KEY_ERROR in data
        if not is_request and not is_resp:
            raise JsonRpc2ComplianceException("Could not determine if data was a request or a response. Please make sure it contains either 'method' to indicate request or 'error' or 'result to indicate response")
        if is_request and is_resp:
            raise JsonRpc2ComplianceException("Data cannot contain 'method' AND either 'error' or 'result': There is no way to determine if this is a request or a response object")
        elif is_request:
            self.validateRequest(data)
        elif is_resp:
            self.validateResponse(data)

    def validateRequest(self, data):
        if JsonRpc2Keys.KEY_PARAMS in data:
            if type(data[JsonRpc2Keys.KEY_PARAMS]) not in [dict, list]:
                raise JsonRpc2ComplianceException("%s must be a dictionary or a list."
                                                  % JsonRpc2Keys.KEY_PARAMS)

    def validateResponse(self, data):
        is_error = JsonRpc2Keys.KEY_ERROR in data
        if is_error:
            errorObj = data[JsonRpc2Keys.KEY_ERROR]
            if type(errorObj) is not dict:
                raise JsonRpc2ComplianceException("Error object must be a dictionary.")
            if JsonRpc2Keys.KEY_ERROR_CODE not in errorObj:
                raise JsonRpc2ComplianceException("Error object is missing %s" % JsonRpc2Keys.KEY_ERROR_CODE)
            if JsonRpc2Keys.KEY_ERROR_MSG not in errorObj:
                raise JsonRpc2ComplianceException("Error object is missing %s" % JsonRpc2Keys.KEY_ERROR_MSG)
            if type(errorObj[JsonRpc2Keys.KEY_ERROR_CODE]) is not int:
                raise JsonRpc2ComplianceException("Error code must be an integer.")
            if type(errorObj[JsonRpc2Keys.KEY_ERROR_MSG]) is not str:
                raise JsonRpc2ComplianceException("Error message must be a string.")
        else:
            if JsonRpc2Keys.KEY_RESULT not in data:
                raise JsonRpc2ComplianceException("%s must be present in response." % JsonRpc2Keys.KEY_RESULT)
