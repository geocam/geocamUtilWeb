# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

# stop pylint from warning us that we "aren't using" imported test cases
# pylint: disable=W0611

from geocamUtil.MultiSettingsTest import MultiSettingsTest
from geocamUtil.anyjsonTest import AnyJsonTest
from geocamUtil.models.UuidFieldTest import UuidFieldTest
from geocamUtil.models.ExtrasFieldTest import ExtrasFieldTest
from geocamUtil.BuilderTest import BuilderTest
from geocamUtil.InstallerTest import InstallerTest
from geocamUtil.icons.rotateTest import IconsRotateTest
from geocamUtil.icons.svgTest import IconsSvgTest

# commandsTest is destructive and should only be run in the example site for geocamUtil
from geocamUtil.management import commandUtil
siteDir = commandUtil.getSiteDir()
print 'siteDir:', siteDir
if siteDir.endswith('geocamUtilWeb/example/'):
    from geocamUtil.management.commandsTest import \
         CollectReqsTest, InstallReqsTest, PrepTemplatesTest, PrepAppsTest, CollectMediaTest
