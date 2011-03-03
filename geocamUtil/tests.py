# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from geocamUtil.MultiSettingsTest import *
from geocamUtil.anyjsonTest import *
from geocamUtil.models.UuidFieldTest import *
from geocamUtil.models.ExtrasFieldTest import *
from geocamUtil.BuilderTest import *
from geocamUtil.InstallerTest import *

# commandsTest is destructive and should only be run in the example site for geocamUtil
from geocamUtil.management import commandUtil
siteDir = commandUtil.getSiteDir()
print 'siteDir:', siteDir
if siteDir.endswith('geocamUtilWeb/example/'):
    from geocamUtil.management.commandsTest import *
