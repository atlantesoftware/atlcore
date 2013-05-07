#coding=UTF-8
from atlcore.contenttype.models.content import Content
from atlcore.contenttype.manager import LocaleManager

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Document(Content):
    
    # fields
    body = models.TextField(_('body'))
    obsolete_date = models.DateField(_('obsolete date'), blank=True, null=True)
    
    # managers    
    # default manager
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    class Meta:
        app_label = 'contenttype'
        verbose_name = _('document')
        verbose_name_plural = _('documents')