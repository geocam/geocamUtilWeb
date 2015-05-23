# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.core import management
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = 'Runs subcommands: installgithooks, preptemplates, prepapps, prepbower, collectstatic -l --noinput, prepcss, collectbinaries'

    def handle_noargs(self, **options):
        #management.call_command('collectreqs')
        #management.call_command('installreqs')
        management.call_command('installgithooks')
        management.call_command('preptemplates')
        management.call_command('prepapps')
        management.call_command('prepbower')
        # manage.py help collectstatic says: -i PATTERN, --ignore=PATTERN Ignore files or directories matching this glob-style pattern. Use multiple times to ignore more.
        management.call_command('collectstatic', interactive=False, link=True)
        management.call_command('prepcss')
        management.call_command('collectbinaries')
