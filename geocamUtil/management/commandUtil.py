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
import itertools

from django.core.management.base import BaseCommand

STATUS_DIR_TEMPLATE = '%(siteDir)s/build/management/commandStatus/'


def getSiteDir():
    # if DJANGO_SETTINGS_MODULE='geocamShare.settings', modImpPath='geocamShare'
    modImpPath = re.sub(r'\..*$', '', os.environ['DJANGO_SETTINGS_MODULE'])
    d = imp.find_module(modImpPath)[1]
    if d != '' and not d.endswith('/'):
        d += '/'
    return d


def getConfirmation(description, default=True, auto=False):
    if default is True:
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
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d)
    f = file(path, 'w')
    f.write(text + '\n')
    f.close()


def writeCommandStatus(commandName, text):
    statusName = getCommandStatusFileName(commandName)
    writeStatusFile(statusName, text)


def getConfirmationUseStatus(commandName, description):
    if getCommandStatus(commandName) is None:
        return True
    else:
        print ('Looks like command %s has finished already, based on file %s'
               % (commandName, getCommandStatusFileName(commandName)))
        return getConfirmation('%s (%s) anyway' % (description, commandName), default=False)


class PathCommand(BaseCommand):
    def handle(self, *args, **options):
        if args:
            # user specified apps to prep
            impPaths = args
        else:
            # user did not specify, default to all apps in INSTALLED_APPS
            from django.conf import settings
            impPaths = settings.INSTALLED_APPS
        self.handleImportPaths(impPaths, options)

    def handleImportPaths(self, impPaths, options):
        pass  # override in derived classes


DEFAULT_LINT_IGNORE_PATTERNS = ['/external/',
                                '/build/',
                                '/doc_src/',
                                '/attic/',
                                '/jquery']
DEFAULT_LINT_IGNORE_REGEXES = [re.compile(pat) for pat in DEFAULT_LINT_IGNORE_PATTERNS]


def parseLintignoreLine(x):
    if x.startswith('#'):
        return []
    elif x.strip() == '':
        return []
    elif x.startswith('\\'):
        return [x[1:]]
    else:
        return [x]


def joinLists(lists):
    return itertools.chain(*lists)


def parseLintignoreText(lintignoreText):
    """
    *lintignoreText* should be the text of a 'lintignore' file. Return
    the corresponding list of regexes to match against file paths.
    """
    lintignoreLines = joinLists([parseLintignoreLine(x)
                                 for x in lintignoreText.splitlines()])
    return [re.compile(x) for x in lintignoreLines]


def pathIsNotIgnored(path, lintignoreRegexes):
    return all([not r.search(path)
                for r in lintignoreRegexes])


def lintignore(pathsText):
    """
    *pathsText* should be a string containing paths separated by
    newlines (like output from the UNIX 'find' command).

    Return a string in the same format, filtering out any paths that
    should be ignored according to the 'lintignore' file.

    Look for the 'lintignore' file at '<site>/management/lintignore'. If
    that file does not exist, use DEFAULT_LINT_IGNORE_PATTERNS.
    """
    lintignorePath = os.path.join(getSiteDir(), 'management', 'lintignore')
    if os.path.exists(lintignorePath):
        lintignoreRegexes = parseLintignoreText(open(lintignorePath, 'r').read())
    else:
        lintignoreRegexes = DEFAULT_LINT_IGNORE_REGEXES

    paths = pathsText.splitlines()
    unignoredFiles = [p for p in paths if pathIsNotIgnored(p, lintignoreRegexes)]
    return '\n'.join(unignoredFiles)
