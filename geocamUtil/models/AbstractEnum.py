
 from django.db import models

class AbstractEnumModel(models.Model):
    class Meta:
        abstract = True
    value = models.CharField(max_length=256)
    display_name = models.CharField( max_length=256, blank=True, null=True )

    def __unicode__(self):
        return self.display_name or self.value
