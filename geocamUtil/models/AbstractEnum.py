# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.db import models

# pylint: disable=C1001


class EnumManager(models.Manager):
    def get_by_natural_key(self, value, display_name):
        return self.get(value=value, display_name=display_name)


class AbstractEnumModel(models.Model):
    objects = EnumManager()
    
    value = models.CharField(max_length=128, unique=True)
    display_name = models.CharField(max_length=256, blank=True, null=True)

    def natural_key(self):
        return (self.value, self.display_name)

    def __unicode__(self):
        return self.display_name or self.value
    
    class Meta:
        abstract = True
        ordering = ['display_name']

