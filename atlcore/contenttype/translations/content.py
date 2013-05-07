#coding=UTF-8
from modeltranslation.translator import translator, TranslationOptions
from atlcore.contenttype.translations import NodeTranslationOptions
from atlcore.contenttype.models import Content

class ContentTranslationOptions(TranslationOptions):
    fields = NodeTranslationOptions.fields
    fields += ('contributor', 'coverage', 'rights', 'subject', )

translator.register(Content, ContentTranslationOptions)
