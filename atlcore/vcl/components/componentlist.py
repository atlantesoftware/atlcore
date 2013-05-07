from atlcore.vcl.components.component import Component

class ComponentList(Component):
    
    def __init__(self, source, driver=None, version=None):
        super(ComponentList, self).__init__(source, driver, version)
        
        