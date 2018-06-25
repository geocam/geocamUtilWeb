#__BEGIN_LICENSE__
# Copyright (c) 2015, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The xGDS platform is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#__END_LICENSE__

# from django.contrib import admin
# import xgds_planner2.models

# this is now an abstract class so if you want it in the admin tool you should register your derived class
# admin.site.register(xgds_planner2.models.Plan)

from django.contrib import admin
from geocamUtil.models import *  # pylint: disable=W0401

admin.site.register(SiteFrame)
