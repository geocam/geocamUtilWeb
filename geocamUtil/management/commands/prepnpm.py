# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the
#Administrator of the National Aeronautics and Space Administration.
#All rights reserved.
# __END_LICENSE__

import os
import subprocess

from django.core.management.base import BaseCommand
from django.apps import apps

def isNpmModule(path):
    return os.path.exists(os.path.join(path, 'package.json'))

class Command(BaseCommand):
    """
    Call bower the first time to install.
    """
    help = 'Install bower components if they have never been installed'

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))

        app_configs = apps.get_app_configs()
        app_paths = [ac.path for ac in app_configs if isNpmModule(ac.path)]

        for path in app_paths:
            print path
            subprocess.Popen(['/usr/bin/npm', 'install'], cwd=path).wait()
