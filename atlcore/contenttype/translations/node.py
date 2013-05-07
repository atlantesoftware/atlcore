#coding=UTF-8
from modeltranslation.translator import translator, TranslationOptions
from atlcore.contenttype.models import Node

class NodeTranslationOptions(TranslationOptions):
    fields = ('title', 'description', )

translator.register(Node, NodeTranslationOptions)
