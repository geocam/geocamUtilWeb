# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the
#Administrator of the National Aeronautics and Space Administration.
#All rights reserved.
# __END_LICENSE__
# __BEGIN_APACHE_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
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
# __END_APACHE_LICENSE__

# stop pylint from warning us that we "aren't using" imported test cases
# pylint: disable=W0611

from geocamUtil.models.timestampDescriptorTest import TimestampDescriptorTest
from geocamUtil.MultiSettingsTest import MultiSettingsTest
from geocamUtil.anyjsonTest import AnyJsonTest
from geocamUtil.models.UuidFieldTest import UuidFieldTest
from geocamUtil.models.ExtrasFieldTest import ExtrasFieldTest
from geocamUtil.models.jsonFieldTest import JsonFieldTest
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
