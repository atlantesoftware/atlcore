#coding=UTF-8
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from atlcore.contenttype.models.content import Content
from atlcore.contenttype.manager import LocaleManager


class Link(Content):
    
    # fields
    url=models.CharField(_('url'), max_length=200)
    icon=models.ImageField(_('icon'), upload_to='links', blank='null')
    open_in_new_page=models.BooleanField(_('open in new page'), default=False)
    
    # managers    
    # default manager
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    def __get_target(self):
        return self.open_in_new_page
    target = property(__get_target)
    
#    def save(self):
#        self.image = self.icon
#        super(Link, self).save()
    
    class Meta:
        app_label = 'contenttype'
        verbose_name = _('link')
        verbose_name_plural = _('links')
        
    def icon_absolute_url(self):
        if self.icon:
            return "%s%s" % (settings.MEDIA_URL, self.icon)

    def get_absolute_url(self):
        return self.url
