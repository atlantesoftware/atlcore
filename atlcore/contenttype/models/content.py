#coding=UTF-8
from atlcore.contenttype.models.node import Node
from atlcore.contenttype.manager import LocaleManager

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Content(Node):
    
    # fields
    contributor=models.CharField(_('contributor'), max_length=256, blank=True, default='')
    coverage=models.CharField(_('coverage'), max_length=256, blank=True, default='')
    creator=models.CharField(_('creator'), max_length=256, blank=True, default='')
    format=models.CharField(_('format'), max_length=256, blank=True, default='')    
    publisher=models.CharField(_('publisher'), max_length=256, blank=True, default='')
    rights=models.TextField(_('rights'), blank=True, default='')
    source=models.CharField(_('source'), max_length=256, blank=True, default='')
    subject=models.CharField(_('subject'), max_length=256, blank=True, default='')
    type=models.CharField(_('type'), max_length=256, blank=True, default='') 
    
    # managers    
    # default manager
    #objects = BaseManager()
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    class Meta:
        app_label = 'contenttype'
