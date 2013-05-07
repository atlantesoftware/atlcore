#encoding=UTF-8
from atlcore.vcl.components.component import Component
from atlcore.settings import MEDIA_URL, JSLIBRARY

class UserSubscriber(Component):
    
    def __init__(self, data_provider=None, version=None, request=None):
        super(UserSubscriber, self).__init__(data_provider, version)
        self.label = 'Email'
        self.submit_button_text = 'Subscribir'
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]
        self._stylelist += [{'user_subscriber': '%svcl/usersubscriber/css/styles.css' % MEDIA_URL}]
    
    