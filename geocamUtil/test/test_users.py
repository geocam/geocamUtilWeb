# __BEGIN_LICENSE__
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
# __END_LICENSE__

from django.test import TestCase
#from django.core.urlresolvers import reverse
#from django.http import HttpResponseForbidden, Http404, JsonResponse
from django.contrib.auth.models import User

from geocamUtil.UserUtil import *


class TestUsers(TestCase):

    fixtures = ['test_users.json']

    """
    Tests for UserUtil.py
    """

    def test_user_exists(self):
        self.assertTrue(user_exists('Bob', 'Wayne'))
        self.assertFalse(user_exists('Bruce', 'Wayne'))

    def test_username_exists(self):
        self.assertTrue(username_exists('bwayne'))
        self.assertFalse(username_exists('ckent'))

    def test_generate_username(self):
        self.assertEqual('bwayne1', get_new_username_from_name('Bruce', 'Wayne'))
        self.assertEqual('pparker', get_new_username_from_name('Peter', 'Parker'))
        self.assertEqual('jvandyne', get_new_username_from_name('Janet', 'van Dyne'))
        self.assertEqual('first', get_new_username_from_name('first'))
        self.assertEqual('first', get_new_username_from_name('first', ''))

    def test_create_user(self):

        # test creating a user that already exists
        result = create_user('Bob', 'Wayne')
        self.assertFalse(result)

        # test creating a user but not saving it
        result = create_user('Gwen', 'Stacy')
        self.assertIsInstance(result, User)
        self.assertIsNone(result.pk)

        # test creating a user and saving it
        result = create_user('MaryJane', 'Watson')
        self.assertIsInstance(result, User)
        self.assertIsNotNone(result.pk)

    def test_get_user_name(self):
        bwayne = User.objects.get(username='bwayne')
        prettyname = getUserName(bwayne)
        self.assertEqual('Bob Wayne', prettyname)

        xgds = User.objects.get(username='xgds')
        prettyname = getUserName(xgds)
        self.assertEqual('xgds', prettyname)

    def test_get_user_by_names(self):
        bwayne = getUserByNames('Bob', 'Wayne')
        self.assertIsNotNone(bwayne)
        self.assertEqual(bwayne.pk, 1)

        bwayneLowers = getUserByNames('bob', 'wayne')
        self.assertIsNotNone(bwayneLowers)
        self.assertEqual(bwayneLowers.pk, 1)

        garbage = getUserByNames('Not', 'There')
        self.assertIsNone(garbage)

    def test_get_user_by_username(self):
        bwayne = getUserByUsername('bwayne')
        self.assertIsNotNone(bwayne)
        self.assertEqual(bwayne.pk, 1)

        bwayneLowers = getUserByUsername('BWAYNE')
        self.assertIsNotNone(bwayneLowers)
        self.assertEqual(bwayneLowers.pk, 1)

        garbage = getUserByUsername('missing')
        self.assertIsNone(garbage)

