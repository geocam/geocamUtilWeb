# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import logging

from geocamUtil.management import commandUtil


class Command(commandUtil.PathCommand):
    help = 'Execute management/appCommands/prep.py for each app in the site'

    def handleImportPaths(self, impPaths, options):
        for impPath in impPaths:
            prepImpPath = '%s.management.appCommands.prep' % impPath

            try:
                appPrepMod = __import__(prepImpPath, fromlist=['dummy'])
            except ImportError:
                appPrepMod = None

            if not appPrepMod:
                logging.debug('skipping %s, could not import %s (check for __init__.py files in directory hierarchy)',
                              impPath, prepImpPath)
                continue

            cmd = appPrepMod.Command()
            cmd.handle(**options)
