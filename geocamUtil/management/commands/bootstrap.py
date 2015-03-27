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

from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Bootstrap submodules and requirements'

    option_list = BaseCommand.option_list + (
        make_option('-r', '--retry',
                    action='store_true',
                    default=False,
                    help='Ask user if they want to re-run steps marked as done'),
        make_option('-y', '--yes',
                    action='store_true',
                    default=False,
                    help='Answer yes to all yes-or-no questions'),
    )

    def handle(self, *args, **options):
        # no op, by the time we get here bootstrapping is done
        pass
