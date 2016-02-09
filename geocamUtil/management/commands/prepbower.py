# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the
#Administrator of the National Aeronautics and Space Administration.
#All rights reserved.
# __END_LICENSE__

import os
import sys
import django
import glob

from optparse import make_option

from django.core.management.base import BaseCommand
from django.core import management

from geocamUtil.management.commandUtil import getSiteDir, dosys
from django.conf import settings


def bowerCompleted(path):
    # since we create the bower_components directory ourselves, the
    # easiest way to check if bower ran properly last time is to look
    # for bower.json files.
    thelist = glob.glob('%s/*/bower.json' % path)
    if thelist:
        installedCount = len(thelist)
        return installedCount != 0
    return False


class Command(BaseCommand):
    """
    Call bower the first time to install.
    """
    help = 'Install bower components if they have never been installed'

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))
        path = os.path.join(settings.BOWER_COMPONENTS_ROOT, "bower_components")
        if not os.path.exists(path):
            # during 'manage.py collectstatic', the djangobower
            # staticfiles finder can fail with an obscure error about
            # missing 'components' directory if the 'bower_components'
            # directory is not present. (older versions of bower used the
            # 'components' directory instead.) what a pain!
            os.makedirs(path)

        if bowerCompleted(path):
            # don't re-run bower if it succeeded before
            return

        management.call_command('bower_install',
                                # avoid interactive prompts that fail under 'vagrant provision'
                                '--',
                                '--config.interactive=false',
                                # continue in spite of conflicting version requirements
                                '--force',
                                *settings.BOWER_INSTALLED_APPS)

        # let's not fail silently
        assert bowerCompleted(path)
