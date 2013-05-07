from atlcore.vcl.components.component import Component

class List(Component):
    
    def __init__(self, source, driver=None, version=None):
        super(List, self).__init__(source, driver, version)
        
        