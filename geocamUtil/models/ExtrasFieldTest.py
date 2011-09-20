# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.test import TestCase

from geocamUtil.models import ExtrasExample


class ExtrasFieldTest(TestCase):
    def setUp(self):
        self.obj = ExtrasExample()
        self.obj.extras.a = 1
        self.obj.extras.b = 'foo'
        self.obj.save()

    def test_recoverContents(self):
        obj2 = ExtrasExample.objects.get(id=self.obj.id)
        self.assertEqual(obj2.extras.a, 1)
        self.assertEqual(obj2.extras.b, 'foo')
