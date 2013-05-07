#coding=UTF-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from atlcore.contenttype.models import Document as DocumentContenttype


class Document(CMSPlugin):
    title = models.CharField('Title', max_length=256, default=None, null=True)
    content = models.ForeignKey(DocumentContenttype, related_name = 'plugins')
    show_title = models.BooleanField(_('Mostrar título'), default=True)
    show_description = models.BooleanField(_('Mostrar descripción'), default=False)
    show_body = models.BooleanField(_('Mostrar cuerpo'), default=False)
    show_image = models.BooleanField(_('Mostrar imagen'), default=False)
    
    def __unicode__(self):
        return self.content.title
