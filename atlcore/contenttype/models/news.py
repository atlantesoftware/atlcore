#coding=UTF-8
from atlcore.contenttype.models.content import Content
from atlcore.contenttype.manager import LocaleManager

from django.db import models
from django.utils.translation import ugettext_lazy as _

class News(Content):
    
    # fields
    body = models.TextField(_('body'))
    
    obsolete_date = models.DateField(_('obsolete date'), blank=True, null=True)
    
    author_photo = models.CharField(_('author photo'), max_length=256, blank=True, null=True)
    
    # managers    
    # default manager
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    class Meta:
        app_label = 'contenttype'
        verbose_name = _('news')
        verbose_name_plural = _('news')