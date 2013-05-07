#coding=UTF-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from atlcore.contenttype.models import News as NewsContenttype


class News(CMSPlugin):
    title = models.CharField('Title', max_length=256, default=None, null=True)
    content = models.ForeignKey(NewsContenttype, related_name = 'plugins')
    show_title = models.BooleanField(_('Mostrar título'), default=True)
    show_description = models.BooleanField(_('Mostrar descripción'), default=False)
    show_body = models.BooleanField(_('Mostrar cuerpo'), default=False)
    show_image = models.BooleanField(_('Mostrar imagen'), default=False)
    
    def __unicode__(self):
        return self.content.title

class NewsList(CMSPlugin):
    title = models.CharField('Title', max_length=256, default=None, null=True)
    amount = models.IntegerField(_("Cantidad a mostrar"), default=1)
    show_image = models.BooleanField(_('Mostrar imagen'), default=False)
    show_description = models.BooleanField(_('Mostrar descripción'), default=False)
    show_paginator = models.BooleanField(_('Mostrar paginador'), default=False)

    def __unicode__(self):
        return self.title

