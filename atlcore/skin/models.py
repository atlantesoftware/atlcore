#coding=UTF-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

class SkinType(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'))
    description = models.TextField(_('description'))
    
    def  __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Skin Type')
        verbose_name_plural = _('Skin Types')      
    
class Skin(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'))
    type = models.ManyToManyField(SkinType, verbose_name=_('skin type'), related_name='%(class)s_related')
    
    def  __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Skin')
        verbose_name_plural = _('Skins')      