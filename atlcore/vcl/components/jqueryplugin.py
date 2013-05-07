#coding=UTF-8
from atlcore.vcl.components import Component

class JQueryPlugin(Component):
    """
        Get a form Field for a database Field that has declared choices.
    """
    
    
    def __init__(self, plugin_name):
        """
        Get a form Field for a database Field that has declared choices.
        """
        super(JQueryPlugin, self).__init__()
        self.plugin_name = plugin_name

    def test(self):
        """ esto es una prueba """
        pass