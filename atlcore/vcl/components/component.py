# coding=UTF-8
#import simplejson as json
from django.utils import simplejson as json
import re

from django.conf import settings
from atlcore.utils.metaclass import no_new_attributes

class Plugin(object):
    
    def __get_config(self): 
        config = {}
        for i in self.__dict__.keys():
            if not re.match('_.', i):
                config[i] = self.__dict__[i]
        return config
    config = property(__get_config)

class Component(object):
    ''' Component generic class 
    
    '''
    
    def __init__(self, data_provider=None, version=None, skin=None):
        ''' 
          En template creamos un diccionario para definir los caminos al template que se
        cargara a la hora de llamar al componente, por defecto se carga el template 'default'
        que apuntará siempre a 'vcl/nombre_del_componente.html'
        ''' 
        self._template = {'default': 'vcl/%s.html' % self.__class__.__name__.lower()}
        self._data_provider = data_provider
        self._version = version
        self._librarylist = []
        self._stylelist = []
        self._config = {}
        self._theme = None
        self._theme_url = 'vcl/%s/css/styles.css' % self.__class__.__name__
        self._skin = skin
        self._id = self.__class__.__name__
        self._html_class = self._id
        self._js_behavior = None
        super(Component, self).__init__()
        
    def __get_template(self): return self._template
    def __set_template(self, value): self._template = value           
    template = property(__get_template, __set_template)
        

    
    def __get_data_provider(self): return self._data_provider
    def __set_data_provider(self, value): self._data_provider = value           
    data_provider = property(__get_data_provider, __set_data_provider)
    source = data_provider # Para mantener compatibilidad con los antiguos componentes
    
    def __get_class_name(self): return self.__class__.__name__
    class_name = property(__get_class_name)
    

    def __get_theme(self): return self._theme
    def __set_theme(self, value): self._theme = value
    theme = property(__get_theme, __set_theme, "Tema visual que se usará para mostrar el objeto")

    def __get_theme_url(self):
        if self._theme: 
            if self._skin:
                return 'skins/%s/vcl/%s/%s/css/styles.css' % (self.skin, self.__class__.__name__.lower(), self._theme)
            else: 
                return 'vcl/%s/%s/css/styles.css' % (self.__class__.__name__.lower(), self._theme)
        else:
            return None
    theme_url = property(__get_theme_url)

    def __get_stylelist(self): return self._stylelist
    def __set_stylelist(self, value): self._stylelist = value
    stylelist = property(__get_stylelist, __set_stylelist, "Tema visual que se usará para mostrar el objeto")

    def __get_skin(self): return self._skin
    def __set_skin(self, value): self._skin = value
    skin = property(__get_skin, __set_skin, "Skin que se usa en el sitio")

    
    def __get_librarylist(self): return self._librarylist
    def __set_librarylist(self, value): self._librarylist = value
    librarylist = property(__get_librarylist, __set_librarylist, "Tema visual que se usará para mostrar el objeto")


    def __get_config(self): 
        config = {}
        for i in self.__dict__.keys():
            if not re.match('_.', i):
                if isinstance(self.__dict__[i], Plugin):
                    config[i] = self.__dict__[i].config
                else:
                    config[i] = self.__dict__[i]
        return json.dumps(config)
    config = property(__get_config)
    
    def __get_id(self): return self._id
    def __set_id(self, value): self._id = value
    id  = property(__get_id, __set_id, 'ID que se le asociará al Tree')

    def __get_html_class(self): return self._html_class
    def __set_html_class(self, value): self._html_class = value
    html_class  = property(__get_html_class, __set_html_class, 'Class que se le asociará al component en el html')


    def __get_js_behavior(self): 
        if self._js_behavior:
            return self._js_behavior
        else:
            from os import path
            js_behavior_url = '%sjs/%s.%s.js' % (settings.MEDIA_URL, self.__class__.__name__, self._id.lower())
            js_behavior_path = '%sjs/%s.%s.js' % (settings.MEDIA_ROOT, self.__class__.__name__, self._id.lower())
            if path.exists(js_behavior_path):
                return js_behavior_url
            else:
                return None
            
    def __set_js_behavior(self, value): self._js_behavior = value
    js_behavior = property(__get_js_behavior, __set_js_behavior, 'Fichero javascript donde se implementa el comportamiento del componente')

