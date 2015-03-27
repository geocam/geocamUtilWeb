# __BEGIN_LICENSE__
#Copyright © 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
#
#The xGDS platform is licensed under the Apache License, Version 2.0 
#(the "License"); you may not use this file except in compliance with the License. 
#You may obtain a copy of the License at 
#http://www.apache.org/licenses/LICENSE-2.0.
#
#Unless required by applicable law or agreed to in writing, software distributed 
#under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
#CONDITIONS OF ANY KIND, either express or implied. See the License for the 
#specific language governing permissions and limitations under the License.
# __END_LICENSE__

import logging
import os
from glob import glob

from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings

from geocamUtil.management import commandUtil
from geocamUtil.Builder import Builder


def dosys(cmd):
    print 'running:', cmd
    os.system(cmd)


def fillTemplate(inputFile, outputFile, context):
    logging.debug('rendering template %s to %s', inputFile, outputFile)
    tmpl = Template(file(inputFile, 'r').read())
    text = tmpl.render(Context(context))
    outDir = os.path.dirname(outputFile)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    file(outputFile, 'w').write(text)


class Command(NoArgsCommand):
    help = "Render site's management/preptemplates/* into build/preptemplates"

    def handle_noargs(self, **options):
        siteDir = commandUtil.getSiteDir()
        builder = Builder()

        context = dict(((k, getattr(settings, k)) for k in dir(settings) if not k.startswith('_')))
        context.update(dict(USER=os.environ['USER']))

        srcs = glob('%smanagement/preptemplates/*' % siteDir)
        for src in srcs:
            dst = '%sbuild/preptemplates/%s' % (siteDir, os.path.basename(src))
            builder.applyRule(dst, [src],
                              lambda: fillTemplate(src, dst, context))
