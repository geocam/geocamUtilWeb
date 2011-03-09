#!/usr/bin/env python
# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os
import sys
import imp
import re

STATUS_DIR_TEMPLATE = '%(siteDir)s/build/management/commandStatus/'

def getSiteDir():
    # if DJANGO_SETTINGS_MODULE='geocamShare.settings', modImpPath='geocamShare'
    modImpPath = re.sub(r'\..*$', '', os.environ['DJANGO_SETTINGS_MODULE'])
    dir = imp.find_module(modImpPath)[1]
    if dir != '' and not dir.endswith('/'):
        dir += '/'
    return dir

def getConfirmation(description, default=True, auto=False):
    if default == True:
        choices = '[Y/n]'
    else:
        choices = '[y/N]'
    prompt = '%s? %s ' % (description, choices)

    if auto:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        if default:
            print 'y'
        else:
            print 'n'
        return default
    else:
        while 1:
            sys.stdout.write(prompt)
            sys.stdout.flush()
            response = raw_input().strip().lower()
            if not response:
                return default
            elif response == 'y':
                return True
            elif response == 'n':
                return False

def getCommandStatusFileName(commandName):
    statusDir = STATUS_DIR_TEMPLATE % dict(siteDir=getSiteDir())
    return '%s%sStatus.txt' % (statusDir, commandName)
    

def getCommandStatus(commandName):
    statusName = getCommandStatusFileName(commandName)
    if os.path.exists(statusName):
        return file(statusName, 'r').read()[:-1]
    else:
        return None

def writeStatusFile(path, text):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    f = file(path, 'w')
    f.write(text + '\n')
    f.close()

def writeCommandStatus(commandName, text):
    statusName = getCommandStatusFileName(commandName)
    writeStatusFile(statusName, text)

def getConfirmationUseStatus(commandName, description):
    if getCommandStatus(commandName) == None:
        return True
    else:
        print ('Looks like command %s has finished already, based on file %s'
               % (commandName, getCommandStatusFileName(commandName)))
        return getConfirmation('%s (%s) anyway' % (description, commandName), default=False)
