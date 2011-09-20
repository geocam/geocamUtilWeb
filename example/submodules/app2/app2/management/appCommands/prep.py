# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.core.management.base import NoArgsCommand

from geocamUtil.management import commandUtil


class Command(NoArgsCommand):
    help = 'Example prep app command'

    def handle_noargs(self, **options):
        print 'running app2 prep command'
        siteDir = commandUtil.getSiteDir()
        commandUtil.writeStatusFile('%sbuild/app2/prepStatus.txt' % siteDir,
                                    'DONE')
