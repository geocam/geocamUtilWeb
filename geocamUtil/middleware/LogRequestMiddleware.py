# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import sys, json, traceback
from settings import CHECKOUT_DIR
from time import time
import os.path

class LogRequestMiddleware(object):
    """
    This class is really the a heavy logging tool, it captures every
    request made to the server and dumps it into a log file in JSON
    """    
    log_file_name = None
    
    def __init__(self):
        # Check to make sure that the logs directory is there, 
        # create the directory if its not there
        self.log_file_name = "%slogs/" % CHECKOUT_DIR
        if os.path.exists(self.log_file_name) == False:
            os.mkdir(self.log_file_name)
        
        # Check to make sure the event.log file is there,
        # create the file if its not there
        self.log_file_name = "%sevents.log" % self.log_file_name
        if os.path.exists(self.log_file_name) == False:
            open(self.log_file_name, 'w').close()
        
    
    def _push_to_log_file(self, data):
        # Convert the entry into a JSON string
        data = json.dumps(data)
        
        # Push the actual log entry to a file
        log_file = open(self.log_file_name, 'a')
        log_file.write(data + '\n')
        log_file.close()
    
    def process_request(self, request):
        log_entry = dict(
            type=request.method,
            path=request.path_info,
            params={},
            authenticated=request.user.is_authenticated(),
            session=request.session.session_key,
            user_id =-1,
            timestamp=time()
        )
        
        # Grab the request params, this might be interesting
        for k,v in request.REQUEST.iteritems():
            log_entry['params'][k] = v
        
        # Grab some basic client request data
        meta_keys = dict(
            user_agent='HTTP_USER_AGENT',
            remote_address='REMOTE_ADDR',
            referer='HTTP_REFERER'
        )
        
        # Iterate through some of the 
        for k,v in meta_keys.iteritems():
            meta_value = None
            
            if request.META.has_key(v):
                meta_value = request.META[v]
            
            log_entry[k] = meta_value
        
        # If the user is authenticated we should add the id
        if log_entry['authenticated'] == True:
            log_entry['user_id'] = request.user.id
        else:
            log_entry['user_id'] = -1
        
        self._push_to_log_file(log_entry)
        
        return None
    