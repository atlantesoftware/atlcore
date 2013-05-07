#coding=UTF-8
from django.db import models
from cms.models import CMSPlugin, Page
from atlcore.contenttype.models import Folder

class AtlGallery(CMSPlugin):
    title = models.CharField('Title', max_length=256, default=None, null=True)
    folder = models.ForeignKey(Folder, related_name = 'plugin')
    album_page = models.ForeignKey(Page, related_name = 'page', null=True)
    
    def __unicode__(self):
        return self.folder.title
