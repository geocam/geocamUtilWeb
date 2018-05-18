# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

# stop pylint from warning us that we "aren't using" imported test cases
# pylint: disable=W0611

from geocamUtil.models.testTimestampDescriptor import TimestampDescriptorTest
from geocamUtil.MultiSettingsTest import MultiSettingsTest
from geocamUtil.anyjsonTest import AnyJsonTest
from geocamUtil.models.testUuidField import UuidFieldTest
from geocamUtil.models.testjsonField import JsonFieldTest
from geocamUtil.BuilderTest import BuilderTest
from geocamUtil.InstallerTest import InstallerTest
from geocamUtil.storeTest import StoreTest
from geocamUtil.icons.rotateTest import IconsRotateTest
from geocamUtil.icons.svgTest import IconsSvgTest

# commandsTest is destructive and should only be run in the example site for geocamUtil
from geocamUtil.management import commandUtil
siteDir = commandUtil.getSiteDir()
print 'siteDir:', siteDir
if siteDir.endswith('geocamUtilWeb/example/'):
    from geocamUtil.management.commandsTest import (CollectReqsTest,
                                                    InstallReqsTest,
                                                    PrepTemplatesTest,
                                                    PrepAppsTest,
                                                    CollectMediaTest)
