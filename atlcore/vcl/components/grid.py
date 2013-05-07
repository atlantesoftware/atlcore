from atlcore.vcl.components.component import Component

class GridNode(object):
    def __init__(self, id, text, url, object, extra=None):
        self.id = id
        self.text = text
        self.url = url
        self.object = object
        self.opts = object._meta
        if extra is not None:
            for key, value in extra.items():
                if hasattr(object, value):
                    attr = getattr(object, value)
                    if callable(attr):
                        try:
                            attr = attr()
                        except:
                            attr = None
                else:
                    attr = None
                setattr(self, value, attr)

class GridDriver(object):
   
    def __iter__(self):
        self.nodes = self.source.__iter__()
        return self    

class Grid(Component):
    def __init__(self, source, driver=None, cols=None):
        self.cols = cols          
        super(Grid, self).__init__(source, driver)
        