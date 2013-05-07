#coding=UTF-8
from atlcore.aspect.fields import AtlAspectForeignKeyField

from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Aspect(models.Model):
    title = models.CharField(_('title'), max_length = 50)
    slug = models.SlugField(_('slug'), default='', blank=True)
    keywords = models.CharField(_('keywords'), default='', max_length = 250, blank=True)
    description = models.TextField(_('description'))
    parent = AtlAspectForeignKeyField('self', verbose_name=_('parent'), null=True, blank=True, related_name='children')
    sites = models.ManyToManyField(Site, related_name='%(class)s_related', verbose_name=_('sites'))
    objects = models.Manager()
    on_site = CurrentSiteManager('sites')
    order=models.PositiveIntegerField(editable=True, default=0, db_index=True)
    
    
    def  __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('aspect')
        verbose_name_plural = _('aspects')    
        
    def get_ancestors(self):
        if self.parent:
            return self.parent.get_ancestors() + [self.parent]
        return []
        

