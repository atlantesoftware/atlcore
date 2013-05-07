#encoding=utf-8

from atlcore.vcl.components import Component
import re
import simplejson as json

class AComponent(Component):
    pass

class test_component(object):
    
    def setup(self):
        self.mycomponent = AComponent()
        self.mycomponent.field1 = 'a'
        self.mycomponent.field2 = 2
        self.mycomponent._hidden_field = 5
        self.mycomponent.boo = True
    
    def test_config_value(self):
        result_json = {'field1': 'a', 'field2': 2, 'boo': True}
        assert self.mycomponent.config == json.dumps(result_json)
        
    def test_template_value(self):
        assert self.mycomponent.template['default'] == 'vcl/acomponent.html'
        