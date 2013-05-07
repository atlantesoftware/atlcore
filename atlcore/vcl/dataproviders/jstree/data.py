#encoding=UTF-8

class JSTreeDataProvider(object):
    
    def __init__(self):
        self.source = None
    
    def __iter__(self):
        self.nodes = self.source.__iter__()
        return self