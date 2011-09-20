# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

import re

from django.test import TestCase

from geocamUtil.models import UuidExample


class UuidFieldTest(TestCase):
    def setUp(self):
        self.u = UuidExample()
        self.u.save()

    def test_format(self):
        self.assert_(re.match(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', self.u.uuid))

    def test_getById(self):
        u2 = UuidExample.objects.get(id=self.u.id)
        self.assertEqual(self.u.uuid, u2.uuid)

    def test_getByUuid(self):
        u2 = UuidExample.objects.get(uuid=self.u.uuid)
        self.assertEqual(self.u.id, u2.id)
