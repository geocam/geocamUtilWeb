# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from optparse import make_option
from django.core.management.base import NoArgsCommand, CommandError

from pip.req import parse_requirements
from glob import glob
import os
import logging

class Foo(object):
    pass

class Command(NoArgsCommand):
    help = 'Collects all app requirements.txt files into build/management/appRequirements.txt'
    
    def handle_noargs(self, **options):
        logger = logging.getLogger('collectreqs')
        logger.setLevel(logging.INFO)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(console)

        # HACK: we expect the test cases to spout warnings, don't want the user to see them and get upset
        if os.environ.has_key('TEST_SUPPRESS_STDERR'):
            console.setLevel(logging.ERROR)

        siteDir = os.path.dirname(os.path.abspath(__import__(os.environ['DJANGO_SETTINGS_MODULE']).__file__))
        logger.debug('siteDir: %s' % siteDir)

        # find app requirements.txt files
        subReqFileList = glob('%s/submodules/*/requirements.txt' % siteDir)
        subReqFiles = dict([(os.path.basename(os.path.dirname(f)), f) for f in subReqFileList])
        logger.debug('subReqFiles: %s' % subReqFiles)

        # parse app requirements.txt files
        subReqs = {}
        opts = Foo()
        opts.skip_requirements_regex = None
        for appName, reqsFile in subReqFiles.iteritems():
            reqs = [entry.req for entry in parse_requirements(reqsFile, options=opts)]
            subReqs[appName] = reqs
        logger.debug('subReqs: %s' % subReqs)

        # calculate maximum version requested for each requirement
        maxVersion = {}
        for appName, reqs in subReqs.iteritems():
            for req in reqs:
                version = req.specs
                maxVersion.setdefault(req.key, version)
                if version > maxVersion[req.key]:
                    maxVersion[req.key] = version

        # write out collected requirements
        outName = '%s/build/management/appRequirements.txt' % siteDir
        outDir = os.path.dirname(outName)
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        out = file(outName, 'w')
        appNames = subReqs.keys()
        appNames.sort()
        reqDone = {}
        for appName in appNames:
            reqs = subReqs[appName]
            out.write('\n# >>>>>>>>>> %s <<<<<<<<<<\n\n' % appName)
            for req in reqs:
                version = req.specs
                if version < maxVersion[req.key]:
                    logger.warning('WARNING: conflict -- app %s wants %s at version %s but another app wants version %s'
                                    % (appName, req.key, version, maxVersion[req.key]))
                    out.write('# %s ... CONFLICT: another app wants a different version!\n' % str(req))
                elif reqDone.has_key(req.key):
                    out.write('# %s ... redundant with entry above\n' % str(req))
                else:
                    out.write('%s\n' % str(req))
                    reqDone[req.key] = True

        logger.info('done collecting requirements')
