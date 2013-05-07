
class LinkSource:
    def __init__(self, text, url):
        self.text = text
        self.url = url

class LinkDrv:
    
    def get_text(self):
        pass
        
    def get_url(self):
        pass

class Link(Component):

    def get_text(self):
        if self.driver:
            return self.driver.get_text()
        else:
            return self.source.text            
        
    def get_url(self):
        if self.driver:
            return self.driver.get_url()
        else:
            return self.source.url
        