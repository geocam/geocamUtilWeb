# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

# pylint: disable=W1401

"""
Creates a new management command 'lint', which runs code checkers to
identify potential problems. Currently it runs pylint and pep8 on
Python files and the Closure Linter (gjslint) on JavaScript files.

Example usage:

 mySite/manage.py lint
   Default: Recursively scans all files below the current directory
 mySite/manage.py lint [dir1] [dir2] ...
   Recursively scans the specified directories

Requirements:

 pip install pylint pep8 http://closure-linter.googlecode.com/files/closure_linter-latest.tar.gz

Tips:

 * Run in a subdirectory. When editing a particular subdirectory, run
   manage.py lint from within that subdirectory to avoid wasting time
   processing irrelevant files.

 * Use editor integration. For example, in Emacs, run manage.py lint
   using M-x compile. That lets you jump straight to the problematic
   source code line. It speeds things up a lot when pep8 gives you
   many niggling whitespace warnings and each fix is a one-character
   edit.

Configuration:

 The following files can be used to customize the checker behavior for
 your site. Find examples in the geocamDjangoSiteSkeleton template.

 mySite/management/pylintrc.txt
 mySite/management/pep8Flags.txt
 mySite/management/gjslintFlags.txt
 mySite/management/lintignore

Editor configuration:

 Whitespace problems are among the most frequent lint warnings. To
 avoid creating them in the first place, set your editor up properly
 for Python:

 * In .emacs:

   (setq-default show-trailing-whitespace t)
   (setq-default indent-tabs-mode nil)

 * In .vimrc:

   set tabstop=4
   set shiftwidth=4
   set expandtab
   match ErrorMsg '\s\+$'

Skip checking files using lintignore:

 Certain files may not be worth checking. Common examples include:
 third-party code, some kinds of generated code, and code that is no
 longer in use (attic).  You can tell lint to ignore certain paths
 by editing mySite/management/lintignore.

Suppressing warnings in pylint:

 Please don't suppress warnings until you understand why the warning
 was there in the first place!

 Sometimes pylint displays bogus warnings because its code analysis is
 not perfect. Other times we suppress warnings because the code is
 known to work and rewriting it would take significant effort and risk
 introducing new bugs. Occasionally we knowingly violate code
 conventions because we think the resulting code is better. If you
 want to suppress a pylint warning, here are some ways:

 1) (Most local) Suppress a specific warning for a single line with an
    inline comment:

    # (tell pylint this wildcard import is ok)
    from geocamUtil.models import *  # pylint: disable=W0401

 2) Suppress a specific warning for the rest of the file:

    def foo():
        # tell pylint we are ok with lots of branches and return statements
        # pylint: disable=R0911,R0912
        ... long function body ...

 3) (Sledge hammer) Suppress a warning for all files in the project by
    editing the 'disable=' line in pylintrc.txt.

Suppressing warnings in pep8:

 Very rarely needed!

 1) Suppress for one line with 'noqa' inline comment:

    some_code_that_pep8_dislikes()  # noqa

 2) Suppress for all lines of a single file. Sorry, there is currently
    no way to do that for pep8.

 3) Suppress for entire project: Edit management/pep8Flags.txt.

Suppressing warnings in gjslint:

 Very rarely needed!

 1) As far as I know you can only suppress errors for the entire project.
    Edit management/gjslintFlags.txt.

"""

import sys

from django.core.management.base import BaseCommand

from geocamUtil.bin.runpylint import runpylint
from geocamUtil.bin.runpep8 import runpep8
from geocamUtil.bin.rungjslint import rungjslint


class Command(BaseCommand):
    help = 'Run code checks (run pylint, pep8 on Python files and gjslint on JavaScript files)'

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', False))

        returnCodes = []
        returnCodes.append(runpylint(args, verbosity=verbosity))
        returnCodes.append(runpep8(args, verbosity=verbosity))
        returnCodes.append(rungjslint(args, verbosity=verbosity))
        errorsFound = not all([c == 0 for c in returnCodes])

        if verbosity > 0:
            if errorsFound:
                print '### manage.py lint done, errors found'
            else:
                print '### manage.py lint done, no errors found'

        sys.exit(errorsFound)
