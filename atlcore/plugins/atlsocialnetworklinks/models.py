#coding=UTF-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from atlcore.contenttype.models import News

class SocialNetworkLinks(CMSPlugin):
    title = models.CharField('Title', max_length=256, default=None, null=True)
    news = models.ForeignKey(News, related_name = 'plugins')
    
    def __unicode__(self):
        return self.news.title

class NewsListBox(CMSPlugin):
    title = models.CharField('Title', max_length=256, default=None, null=True)
    max_element = models.IntegerField(_("Noticias a mostrar"), default=1)
    show_image = models.BooleanField(_('Mostrar imagen'), default=False)
    show_description = models.BooleanField(_('Mostrar descripción'), default=False)
    show_paginator = models.BooleanField(_('Mostrar paginador'), default=False)
    
    def __unicode__(self):
        return self.title