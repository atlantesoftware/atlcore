#coding=UTF-8
from modeltranslation.translator import translator, TranslationOptions
from atlcore.contenttype.translations import ContainerTranslationOptions
from atlcore.contenttype.models import Folder

class FolderTranslationOptions(TranslationOptions):
    fields = ContainerTranslationOptions.fields

translator.register(Folder, FolderTranslationOptions)
