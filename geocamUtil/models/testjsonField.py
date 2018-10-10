# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.test import TransactionTestCase

from geocamUtil.models import JsonExample


class JsonFieldTest(TransactionTestCase):
    def setUp(self):
        self.obj = JsonExample()
        self.obj.intChar = [3, -4]
        self.obj.floatChar = [5.1, -6.2]
        self.obj.intText = [3, -4]
        self.obj.floatText = [5.1, -6.2]
        self.obj.save()

    def test_recoverContents(self):
        obj2 = JsonExample.objects.get(id=self.obj.id)
        self.assertEqual(obj2.intChar, self.obj.intChar)
        self.assertEqual(obj2.floatChar, self.obj.floatChar)
        self.assertEqual(obj2.intText, self.obj.intText)
        self.assertEqual(obj2.floatText, self.obj.floatText)
