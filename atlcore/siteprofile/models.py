#coding=UTF-8
from atlcore.skin.models import Skin

from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

class SiteProfile(models.Model):
    site = models.OneToOneField(Site, verbose_name=_('site'), related_name='profile')
    keywords = models.CharField(_('keywords'), max_length=250)
    description = models.TextField(_('description'))
    facebook = models.URLField(blank=True)
    twitter = models.CharField(blank=True, max_length=250)
    contact = models.EmailField(_('contact email'), blank=True)
    google_analytics_script = models.TextField(_('Google Analytics Script'), blank=True)

    #Logo
    logo_height = models.FloatField(blank=True, null=True, editable=False)
    logo_width = models.FloatField(blank=True, null=True, editable=False)
    logo = models.ImageField(upload_to='sites_images', height_field='logo_height', width_field='logo_width', blank=True)
    #favicon
    favicon_height = models.FloatField(blank=True, null=True, editable=False)
    favicon_width = models.FloatField(blank=True, null=True, editable=False)
    favicon = models.ImageField(upload_to='sites_images', height_field='favicon_height', width_field='favicon_width', blank=True)
    
    skin = models.ForeignKey(Skin, verbose_name=_('skin'), related_name='site_profile', blank=True, null=True)    
    #Manejador por defecto
    objects = models.Manager()
    
    def  __unicode__(self):
        return u"%s profile" %self.site.name

    class Meta:
        verbose_name = _('Site Profile')
        verbose_name_plural = _('Sites Profile')        
