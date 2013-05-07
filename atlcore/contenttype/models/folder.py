#coding=UTF-8
from atlcore.contenttype.models.container import Container
from atlcore.contenttype.manager import LocaleManager

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Folder(Container):
    
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    class Meta:
        app_label = 'contenttype'
        verbose_name = _('folder')
        verbose_name_plural = _('folders')