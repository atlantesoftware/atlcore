#coding=UTF-8
from atlcore.contenttype.models.content import Content
from atlcore.contenttype.manager import LocaleManager

from django.db import models
from django.utils.translation import ugettext_lazy as _

class File(Content):
    
    # fields
    file=models.FileField (_("file"), upload_to="files/")
     
    # managers    
    # default manager
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    
    def get_file_url(self):
        if self.file:
            return self.file.url
        
    def get_absolute_url(self):
        if self.file:
            return self.file.url
    
    class Meta:
        app_label = 'contenttype'
        verbose_name = _('file')
        verbose_name_plural = _('files')