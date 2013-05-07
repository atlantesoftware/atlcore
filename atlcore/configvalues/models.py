#coding=UTF-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from atlcore.utils.guid import get_guid
from atlcore.libs.stdimage import StdImageField

IMAGE_SIZE = (640, 480)
THUMBNAIL_SIZE = (100, 100, True)

class ConfigValues(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=get_guid)
    name = models.CharField(_('Name'), max_length=200, unique=True)
    value = models.CharField(_('Value'), max_length=200)
    
    def __unicode__(self):
        return self.name