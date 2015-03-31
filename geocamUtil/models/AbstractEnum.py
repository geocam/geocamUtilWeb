# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.db import models

# pylint: disable=C1001


class AbstractEnumModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['display_name']
    value = models.CharField(max_length=256)
    display_name = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return self.display_name or self.value
