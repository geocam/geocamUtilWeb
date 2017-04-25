# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    
    help = 'Bootstrap submodules and requirements'

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--retry',
            action='store_true',
            default=False,
            help='Ask user if they want to re-run steps marked as done',
        )
        
        parser.add_argument(
            '--yes',
            action='store_true',
            default=False,
            help='Answer yes to all yes-or-no questions',
        )


    def handle(self, *args, **options):
        # no op, by the time we get here bootstrapping is done
        pass
