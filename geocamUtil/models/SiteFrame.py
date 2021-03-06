# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
# __END_LICENSE__

from django.db import models

class SiteFrame(models.Model):
    name = models.CharField(max_length=128)
    displayName = models.CharField(max_length=128)
    east0 = models.FloatField()
    north0 = models.FloatField()
    zone = models.CharField(max_length=8)
    zoneNumber = models.IntegerField()
    south = models.BooleanField()
    axes = models.CharField(max_length=8, default='ENU')
    north = models.CharField(max_length = 8)
    timezone = models.CharField(max_length=64)
    projCode = models.CharField(max_length=32, null=True)
    projString = models.CharField(max_length=512, null=True)
    projUnits = models.CharField(max_length=32, default="m")
    
    def __unicode__(self):
        return self.displayName

    class Meta:
        app_label="geocamUtil"
