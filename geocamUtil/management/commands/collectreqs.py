# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.core.management.base import NoArgsCommand, CommandError

from pip.req import parse_requirements
from glob import glob
import os
import logging

from geocamUtil.Builder import Builder
from geocamUtil.management import commandUtil

class Foo(object):
    pass

class Command(NoArgsCommand):
    help = 'Collect all app requirements.txt files and siteRequirements.txt into allRequirements.txt'
    
    def getSrcName(self, reqFile):
        if os.path.basename(reqFile) == 'siteRequirements.txt':
            return '00_site'
        else:
            return os.path.basename(os.path.dirname(reqFile))

    def collect(self, outName, subReqFileList):
        subReqFiles = dict([(self.getSrcName(f), f) for f in subReqFileList])
        self.logger.debug('subReqFiles: %s' % subReqFiles)

        # parse app requirements.txt files
        subReqs = {}
        opts = Foo()
        opts.skip_requirements_regex = None
        for srcName, reqsFile in subReqFiles.iteritems():
            reqs = [entry.req for entry in parse_requirements(reqsFile, options=opts)]
            subReqs[srcName] = reqs
        self.logger.debug('subReqs: %s' % subReqs)

        # calculate maximum version requested for each requirement
        maxVersion = {}
        for srcName, reqs in subReqs.iteritems():
            for req in reqs:
                version = req.specs
                maxVersion.setdefault(req.key, version)
                if version > maxVersion[req.key]:
                    maxVersion[req.key] = version

        # write out collected requirements
        outDir = os.path.dirname(outName)
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        out = file(outName, 'w')
        srcNames = subReqs.keys()
        srcNames.sort()

        out.write('# This file is auto-generated, do not modify!\n')
        out.write('#\n')
        out.write('# source files:\n')
        out.write('#\n')
        for srcName in srcNames:
            out.write('#   %s = %s\n' % (srcName, subReqFiles[srcName]))
        out.write('\n')
        reqDone = {}
        for srcName in srcNames:
            reqs = list(subReqs[srcName])
            reqs.sort(key=lambda r: r.key)
            out.write('\n# >>>>>>>>>> %s <<<<<<<<<<\n\n' % srcName)
            for req in reqs:
                version = req.specs
                if version < maxVersion[req.key]:
                    self.logger.warning('WARNING: conflict -- module %s wants %s at version %s but another module wants version %s'
                                        % (srcName, req.key, version, maxVersion[req.key]))
                    out.write('# %s ... CONFLICT: another app wants a different version!\n' % str(req))
                elif reqDone.has_key(req.key):
                    out.write('# %s ... redundant with entry above\n' % str(req))
                else:
                    out.write('%s\n' % str(req))
                    reqDone[req.key] = True

        self.logger.info('done collecting requirements')

    def handle_noargs(self, **options):
        self.logger = logging.getLogger('collectreqs')
        self.logger.setLevel(logging.INFO)
        
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console)

        # HACK: we expect the test cases to spout warnings, don't want the user to see them and get upset
        if os.environ.has_key('TEST_SUPPRESS_STDERR'):
            console.setLevel(logging.ERROR)

        siteDir = commandUtil.getSiteDir()
        self.logger.debug('siteDir: %s' % siteDir)
        outName = '%s/build/management/allRequirements.txt' % siteDir

        subReqFileList = (glob('%ssubmodules/*/requirements.txt' % siteDir)
                          + glob('%sapps/*/management/requirements.txt' % siteDir)
                          + glob('%smanagement/siteRequirements.txt' % siteDir))
        
        builder = Builder()
        builder.applyRule(outName, subReqFileList,
                          lambda: self.collect(outName, subReqFileList))
