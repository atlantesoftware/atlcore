#encoding=UTF-8
from atlcore.vcl.components import Component

class Anchor(Component):
    
    def __init__(self, text, href):
        self.href = href
        self.text = text   
