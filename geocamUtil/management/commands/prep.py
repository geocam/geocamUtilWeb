# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Runs subcommands: installgithooks, preptemplates, prepapps, prepbower, collectstatic -l --noinput, prepcss, collectbinaries'

    def handle(self, *args, **options):
#         management.call_command('installgithooks')
        
#         management.call_command('prepmigrations')
#         management.call_command('migrate --fake-initial')
#         management.call_command('prepfixtures')
                
        management.call_command('preptemplates')
        management.call_command('prepapps')
        management.call_command('prepbower')
        management.call_command('prepbrowserify')
        # manage.py help collectstatic says: -i PATTERN, --ignore=PATTERN Ignore files or directories matching this glob-style pattern. Use multiple times to ignore more.
        management.call_command('collectstatic', interactive=False, link=True)
        management.call_command('prepcss')
        management.call_command('collectbinaries')
