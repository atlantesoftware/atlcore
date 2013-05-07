# encoding = UTF-8

class MediaEnvironment(object):
    
    def __init__(self):
        self._styles = []
        self._scripts = []
    
    def append_style(self, style):
        if not style in self._styles:
            self._styles.append(style)
    
    def append_script(self, script):
        if not script in self._scripts:
            self._scripts.append(script)
            
    def append_media(self, component):
        for style in component.stylelist:
            self.append_style(style)
        for script in component.librarylist:
            self.append_script(script)
        if component.theme:
            self.append_style({'%s_theme-%s' % (component.class_name, component.theme): component.theme_url})
            
    def __get_styles(self): return self._styles
    styles = property(__get_styles)
    
    def __get_scripts(self): return self._scripts
    scripts = property(__get_scripts)
    