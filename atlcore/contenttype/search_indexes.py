# -*- coding: utf-8 -*-
import datetime
from haystack.indexes import *
from haystack import site
from atlcore.contenttype.models import News, Video, Document


class NewsIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    
    def get_queryset(self):
        """
        This is used when the entire index for model is updated, and should only include
        public entries
        """
        return News.objects.filter(updated_on__lte=datetime.datetime.now(), state='Public')

class VideoIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    
    def get_queryset(self):
        """
        This is used when the entire index for model is updated, and should only include
        public entries
        """
        return Video.objects.filter(updated_on__lte=datetime.datetime.now(), state='Public')

class DocumentIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    
    def get_queryset(self):
        """
        This is used when the entire index for model is updated, and should only include
        public entries
        """
        return Document.objects.filter(updated_on__lte=datetime.datetime.now(), state='Public')


site.register(News, NewsIndex)
site.register(Video, VideoIndex)
site.register(Document, DocumentIndex)
