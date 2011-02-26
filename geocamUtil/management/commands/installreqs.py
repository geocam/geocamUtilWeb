from optparse import make_option
from django.core.management.base import NoArgsCommand, CommandError

import os

class Command(NoArgsCommand):
    help = 'Uses pip to install requirements found in management/requirements.txt'
    
    def handle_noargs(self, **options):
        siteDir = os.path.dirname(os.path.abspath(__import__(os.environ['DJANGO_SETTINGS_MODULE']).__file__))
        os.system('pip install -r %s/management/requirements.txt' % siteDir)
