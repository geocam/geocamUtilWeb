# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

"""
Creates a new management command 'lint', which runs code checkers to
identify potential problems. Currently it runs pylint and pep8 on
Python files and JavaScript Lint (jsl) on JavaScript files.

Example usage:

 mySite/manage.py lint
   Default: Recursively scans all files below the current directory
 mySite/manage.py lint *.py
   Scans the specified files

Requirements:

 Needs the pep8 and pylint modules available through 'pip install'.
 JavaScript Lint is available at http://www.javascriptlint.com/ .

Configuration:

 The following files can be used to customize the checker behavior for
 your site. Find examples in the geocamDjangoSiteSkeleton template.

 mySite/management/pylintrc.txt
 mySite/management/pep8Flags.txt
 mySite/management/jslrc.txt

Tips:

 Sometimes pylint displays bogus warnings. Other times we knowingly
 violate code conventions because we think the resulting code is better.
 If you want to suppress a pylint warning, here are some ways:

 1) (Best) Suppress a specific warning for a single line with an
    inline comment:

    # (tell pylint this wildcard import is ok)
    from geocamUtil.models import *  # pylint: disable=W0401

 2) Suppress a specific warning in the subsequent code:

    def foo():
        # tell pylint we are ok with lots of branches and return statements
        # pylint: disable=R0911,R0912
        ... long function body ...

 3) (Use with caution) Suppress a warning for all files by editing the
    'disable=' line in pylintrc.txt.
"""

from django.core.management.base import BaseCommand

from geocamUtil.bin.runpylint import runpylint
from geocamUtil.bin.runpep8 import runpep8
from geocamUtil.bin.runjsl import runjsl


class Command(BaseCommand):
    help = 'Run code checks (run pylint, pep8 on Python files and jsl on JavaScript files)'

    def handle(self, *args, **options):
        runpylint(args)
        runpep8(args)
        runjsl(args)
