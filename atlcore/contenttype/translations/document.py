#coding=UTF-8
from modeltranslation.translator import translator, TranslationOptions
from atlcore.contenttype.translations import ContentTranslationOptions
from atlcore.contenttype.models import Document

class DocumentTranslationOptions(TranslationOptions):
    fields = ContentTranslationOptions.fields
    fields += ('body',)


translator.register(Document, DocumentTranslationOptions)
