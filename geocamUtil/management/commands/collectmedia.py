# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import os
import logging

import django

from geocamUtil.management import commandUtil
from geocamUtil.Installer import Installer
from geocamUtil import settings


class Command(commandUtil.PathCommand):
    help = 'Collect static files from all apps into STATIC_ROOT'

    def handleImportPaths(self, impPaths, options):
        inst = Installer()
        siteDir = commandUtil.getSiteDir()

        # make new-style static and media setup
        staticRoot = getattr(settings, 'STATIC_ROOT', '%sbuild/static' % siteDir)
        if not os.path.exists(staticRoot):
            os.makedirs(staticRoot)
        #if not os.path.exists(settings.MEDIA_ROOT):
        #    mediaRootNoTrailingSlash = re.sub('/$', '', settings.MEDIA_ROOT)
        #    os.symlink(staticRoot, mediaRootNoTrailingSlash)

        # install admin media
        djangoDir = os.path.dirname(os.path.realpath(django.__file__))
        adminMediaDir = os.path.join(djangoDir, 'contrib', 'admin', 'media')
        inst.installRecurse(adminMediaDir, os.path.join(staticRoot, 'admin'))

        for impPath in impPaths:
            logging.debug('collectmedia app %s', impPath)
            appMod = __import__(impPath, fromlist=['dummy'])
            appPath = os.path.dirname(appMod.__file__)
            tryMediaPaths = ['%s/build/static' % appPath,
                             '%s/build/media' % appPath,  # legacy support
                             '%s/static' % appPath]
            for mediaPath in tryMediaPaths:
                logging.debug('collectmedia app %s: checking for media in %s', impPath, mediaPath)
                if os.path.exists(mediaPath):
                    inst.installRecurseGlob('%s/*' % mediaPath, '%sbuild/static' % siteDir)
                    break
