# __BEGIN_LICENSE__
#Copyright © 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
#
#The xGDS platform is licensed under the Apache License, Version 2.0 
#(the "License"); you may not use this file except in compliance with the License. 
#You may obtain a copy of the License at 
#http://www.apache.org/licenses/LICENSE-2.0.
#
#Unless required by applicable law or agreed to in writing, software distributed 
#under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
#CONDITIONS OF ANY KIND, either express or implied. See the License for the 
#specific language governing permissions and limitations under the License.
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

        management.call_command('bower', 'install', verbosity=verbosity)
