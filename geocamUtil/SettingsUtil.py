# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__


import socket
try:
    HOSTNAME = socket.gethostname()
except:
    HOSTNAME = 'localhost'


INDEX = {}

def getOrCreateDict(dictName):
    if dictName not in INDEX:
        INDEX[dictName] = {}
    return INDEX[dictName]
        
def getOrCreateArray(arrayName):
    if arrayName not in INDEX:
        INDEX[arrayName] = []
    return INDEX[arrayName]
    
