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
from datetime import datetime

# J2000 is seconds from 1/1/2000 at 0:00:00
class J2000:
    def __init__(self, value):
        self.value = value

    def toUnixDate(self):
        return self.value + 946684800.0

    def to_datetime(self):
        ud = self.toUnixDate()
        full_datetime = datetime.utcfromtimestamp(ud)
        return full_datetime
