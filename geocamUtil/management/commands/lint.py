# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from optparse import make_option

from django.core.management.base import BaseCommand

from geocamUtil.bin.runpylint import runpylint
from geocamUtil.bin.runpep8 import runpep8
from geocamUtil import settings

class Command(BaseCommand):
    help = 'Run pylint and pep8 on Python files'

    def handle(self, *args, **options):
        runpylint(settings.CHECKOUT_DIR)
        runpep8(settings.CHECKOUT_DIR)
