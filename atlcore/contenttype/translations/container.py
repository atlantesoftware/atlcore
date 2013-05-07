#coding=UTF-8
from modeltranslation.translator import translator, TranslationOptions
from atlcore.contenttype.translations import ContentTranslationOptions
from atlcore.contenttype.models import Container

class ContainerTranslationOptions(TranslationOptions):
    fields = ContentTranslationOptions.fields

translator.register(Container, ContainerTranslationOptions)
