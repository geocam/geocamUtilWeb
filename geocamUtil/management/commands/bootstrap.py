# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
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
