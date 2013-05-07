#coding=UTF-8
from atlcore.contenttype.models.content import Content
from atlcore.contenttype.manager import LocaleManager

from django.db import models
from django.utils.translation import ugettext_lazy as _
#from atlcore import settings #Revisar, esto se quita para que no hayan imports circulares

RESOURCES_CHOICES = (
    ('Image', _('Image')),
    ('Flash', 'Flash'),
)
DEFAULT_RESOURCE = RESOURCES_CHOICES[0][0]

class Banner(Content):
    
    # fields
    url=models.CharField(_('url'), max_length=200)
    obsolete_date=models.DateField(_("obsolete date"), blank=True, null=True)
    resource_type=models.CharField(_("resource type"), max_length=20, choices=RESOURCES_CHOICES, default=DEFAULT_RESOURCE)
    image=models.ImageField(_('image'), upload_to='posters', blank=True)
    flash=models.FileField (_("flash"), upload_to='posters', blank=True)
    width=models.PositiveIntegerField(_('width'), default=0)
    height=models.PositiveIntegerField(_('height'), default=0)
    open_in_new_page=models.BooleanField(_('open in new page'), default=False)
    # managers    
    # default manager
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    class Meta:
        app_label = 'contenttype'
        verbose_name = _('banner')
        verbose_name_plural = _('banners')
        
    def get_absolute_url(self):
        return self.url