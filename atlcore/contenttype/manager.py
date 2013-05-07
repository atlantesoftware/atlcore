#coding=UTF-8
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import get_language

class LocaleManager(models.Manager):

    def get_query_set(self):
        return super(LocaleManager, self).get_query_set().filter(state = "Public").filter(language = get_language())

class BaseManager(models.Manager):
     
    def by_models(self, list):
        cts = [ContentType.objects.get_for_model(model) for model in list]
        return self.get_query_set().filter(content_type__in=cts)
 
    def by_models_name(self, list):   
        cts = ContentType.objects.none()
        for model_name in list:
            cts |= ContentType.objects.filter(app_label='contenttype', model=model_name)
        return self.get_query_set().filter(content_type__in=cts)