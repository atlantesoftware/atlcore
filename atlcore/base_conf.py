#coding=UTF-8
from os.path import abspath, dirname, join

DIRECTORY = abspath(dirname(__file__))
MEDIA_URL = '/atlante_core_media/'
MEDIA_PREFIX = 'media/'
MEDIA_ROOT = join(abspath(DIRECTORY), MEDIA_PREFIX)

# Directorio donde se ponen los ficheros que se suben por los formularios de los contenidos
