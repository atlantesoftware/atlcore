#coding=UTF-8
from atlcore.contenttype.models.content import Content
from atlcore.contenttype.manager import LocaleManager

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Picture(Content):
    
    # fields
    
    # managers    
    # default manager
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    class Meta:
        app_label = 'contenttype'
        verbose_name = _('picture')
        verbose_name_plural = _('pictures')
