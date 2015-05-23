# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

import os
import sys
import django

from optparse import make_option

from django.core.management.base import BaseCommand
from django.core import management

from geocamUtil.management.commandUtil import getSiteDir, dosys
from geocamUtil import settings


class Command(BaseCommand):
    """
    Call bower the first time to install.
    """
    help = 'Install bower components if they have never been installed'

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))
        path = os.path.join(settings.BOWER_COMPONENTS_ROOT, "bower_components")
        if os.path.isdir(path):
            return

        management.call_command('bower_install', verbosity=verbosity, force=True)
