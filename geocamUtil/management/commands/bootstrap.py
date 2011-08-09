# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.core import management
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = 'Bootstrap submodules and requirements'
    
    def handle_noargs(self, **options):
        # no op, by the time we get here bootstrapping is done
        pass
