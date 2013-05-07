#coding=UTF-8

class ComponentVersionError(Exception):
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return 'Error de versión: El componente no implementa la versión especificada'
