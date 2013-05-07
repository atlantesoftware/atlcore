#encoding=UTF-8
from atlcore.vcl.components import Component

class Image(Component):
    
    def __init__(self, src, alt=None, url=None, target=None):
        super(Image, self).__init__()
        self.src = src
        self.alt = alt   
        self.url = url 
        self.target = target
