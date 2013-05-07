#coding=UTF-8
from modeltranslation.translator import translator, TranslationOptions
from atlcore.contenttype.translations import ContentTranslationOptions
from atlcore.contenttype.models import News

class NewsTranslationOptions(TranslationOptions):
    fields = ContentTranslationOptions.fields
    fields += ('body',)
    #fallback_values = {'content': 'no data'}

translator.register(News, NewsTranslationOptions)
