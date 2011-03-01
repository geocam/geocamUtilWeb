# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import logging
from glob import glob

from django.core.management.base import BaseCommand

from geocamUtil.management import commandUtil

class Command(BaseCommand):
    help = 'Execute management/appCommands/prep.py for each app in the site'

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
            prepImpPath = '%s.management.appCommands.prep' % impPath

            try:
                appPrepMod = __import__(prepImpPath, fromlist=['dummy'])
            except ImportError:
                appPrepMod = None

            if not appPrepMod:
                logging.debug('skipping %s, does not define management/appCommands/prep.py' % prepImpPath)
                continue

            cmd = appPrepMod.Command()
            cmd.handle(**options)
