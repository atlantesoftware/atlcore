

class Menu(object):
    
    def __init__(self, title, items):
        self.title = title
        self.items = items

    def get_items(self):
        return self.items


class Menu_Vertical(Menu):
    pass

class Menu_Horizontal(Menu):
    pass

class Tree(Menu):
    pass

class Carousel(object):
    pass

class PageObjects(object):
    pass
