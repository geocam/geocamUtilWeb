# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.core import management
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = 'Runs subcommands: preptemplates, prepapps, collectmedia'

    def handle_noargs(self, **options):
        #management.call_command('collectreqs')
        #management.call_command('installreqs')
        management.call_command('preptemplates')
        management.call_command('prepapps')
        management.call_command('collectmedia')
        management.call_command('collectbinaries')
