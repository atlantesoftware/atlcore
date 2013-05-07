#coding=UTF-8
from modeltranslation.translator import translator, TranslationOptions
from atlcore.contenttype.translations import ContentTranslationOptions
from atlcore.contenttype.models import Banner

class BannerTranslationOptions(TranslationOptions):
    fields = ContentTranslationOptions.fields

translator.register(Banner, BannerTranslationOptions)
