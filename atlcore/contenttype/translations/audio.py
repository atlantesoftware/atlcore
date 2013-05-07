#coding=UTF-8
from modeltranslation.translator import translator, TranslationOptions
from atlcore.contenttype.translations import ContentTranslationOptions
from atlcore.contenttype.models import Audio

class AudioTranslationOptions(TranslationOptions):
    fields = ContentTranslationOptions.fields

translator.register(Audio, AudioTranslationOptions)
