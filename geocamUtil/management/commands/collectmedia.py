# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os
import logging

from geocamUtil.management import commandUtil
from geocamUtil.Installer import Installer


class Command(commandUtil.PathCommand):
    help = 'Collect media from all apps into build/media'

    def handleImportPaths(self, impPaths, options):
        for impPath in impPaths:
            logging.debug('collectmedia app %s', impPath)
            appMod = __import__(impPath, fromlist=['dummy'])
            appPath = os.path.dirname(appMod.__file__)
            tryMediaPaths = ['%s/build/media' % appPath,
                             '%s/static' % appPath]
            for mediaPath in tryMediaPaths:
                logging.debug('collectmedia app %s: checking for media in %s', impPath, mediaPath)
                if os.path.exists(mediaPath):
                    siteDir = commandUtil.getSiteDir()
                    inst = Installer()
                    inst.installRecurseGlob('%s/*' % mediaPath, '%sbuild/media' % siteDir)
                    break
