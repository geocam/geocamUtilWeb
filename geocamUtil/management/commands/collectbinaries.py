# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import os
import logging
from glob import glob

from django.core.management.base import BaseCommand

from geocamUtil.management import commandUtil
from geocamUtil.Installer import Installer

class Command(BaseCommand):
    help = 'Collect binaries from all apps into build/bin'

    def handle(self, *args, **options):
        from django.db import models
        if args:
            # user specified apps to prep
            impPaths = args
        else:
            # user did not specify, default to all apps in INSTALLED_APPS
            from django.conf import settings
            impPaths = settings.INSTALLED_APPS

        for impPath in impPaths:
            logging.debug('collectbinaries app %s' % impPath)
            appMod = __import__(impPath, fromlist=['dummy'])
            appPath = os.path.dirname(appMod.__file__)
            binPath = '%s/bin' % appPath
            logging.debug('collectbinaries app %s: checking for binaries in %s' % (impPath, binPath))
            if os.path.exists(binPath):
                siteDir = commandUtil.getSiteDir()
                inst = Installer()
                inst.installRecurseGlob('%s/*' % binPath, '%sbuild/bin' % siteDir)
