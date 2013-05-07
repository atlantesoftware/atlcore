#encoding=UTF-8
from atlcore.vcl.components.component import Component
from django.conf import settings
from django.utils.translation import get_language
from atlcore.settings import JSLIBRARY

class LanguageSwitch(Component):
    
    def __init__(self, data_provider=None,  version=None):
        super(LanguageSwitch, self).__init__(data_provider, version)
        self.LANGUAGES = settings.LANGUAGES
        self.LANGUAGE = get_language()
        self._librarylist += [{'lib_languageswitch' : JSLIBRARY['lib_languageswitch']}] 
