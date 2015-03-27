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

from django.core import management
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = 'Runs subcommands: installgithooks, preptemplates, prepapps, collectmedia, prepcss -c, collectstatic -l, collectbinaries'

    def handle_noargs(self, **options):
        #management.call_command('collectreqs')
        #management.call_command('installreqs')
        management.call_command('installgithooks')
        management.call_command('preptemplates')
        management.call_command('prepapps')
        management.call_command('prepbower')
        management.call_command('collectstatic', noinput=True, link=True)
        management.call_command('prepcss')
        management.call_command('collectbinaries')
