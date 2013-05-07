#coding=UTF-8
from atlcore.base_conf import DIRECTORY as BASE_DIRECTORY, MEDIA_URL as BASE_MEDIA_URL, MEDIA_ROOT as BASE_MEDIA_ROOT

from django.conf import settings
from django.utils.translation import ugettext as _
from os.path import abspath, dirname, join

DIRECTORY = getattr(settings, "ATLANTE_CMS_DIR", BASE_DIRECTORY)

CONTENT_MEDIA_DIRECTORY ='content_files/' 

ADMIN_PREFIX = getattr(settings, "ATL_ADMIN_PREFIX", 'atlcms')

ADMIN_ELEMENT_BY_PAGE = getattr(settings, "ATLANTE_ADMIN_ELEMENT_BY_PAGE", 20)

THEME = 'atlcms'

# Note: If you change this URL, you also have to change the file urls.py.
MEDIA_URL = getattr(settings, "ATLANTE_CMS_MEDIA_URL", BASE_MEDIA_URL)

MEDIA_ROOT = BASE_MEDIA_ROOT
STATIC_URL = settings.STATIC_URL

RELEVANT_STATISTIC_DAYS_NUMBER = getattr(settings, "ATLANTE_CMS_RELEVANT_STATISTIC_DAYS_NUMBER", 7)

LANGUAGES = getattr(settings, "LANGUAGES", (('es', _('Spanish')),('en', _('English')))) 

LANGUAGE_CODE = getattr(settings, "LANGUAGE_CODE", 'es')

JSLIBRARY = {
    'lib_atlcore': 'common/js/atlcore.js',
    'lib_jquery': 'common/jquery/jquery-1.5.1.min.js',
    'lib_jquery.layout': 'common/js/jquery.layout.js',
    'lib_jquery.ui.core': 'common/jquery/ui/v1.8.13/jquery.ui.core.min.js',
    'lib_jquery.ui.widget': 'common/jquery/ui/v1.8.13/jquery.ui.widget.min.js',
    'lib_jquery.ui.mouse': 'common/jquery/ui/v1.8.13/jquery.ui.mouse.min.js',
    'lib_jquery.ui.sortable': 'common/jquery/ui/v1.8.13/jquery.ui.sortable.min.js',
    'lib_jquery.ui.droppable': 'common/jquery/ui/v1.8.13/jquery.ui.droppable.min.js',
    'lib_jquery.ui.draggable': 'common/jquery/ui/v1.8.13/jquery.ui.draggable.min.js',
    'lib_jquery.ui.button': 'common/jquery/ui/v1.8.13/jquery.ui.button.min.js',
    'lib_jquery.history': 'common/js/jquery.history.js',
    'lib_jquery.opacityrollover': 'common/js/jquery.opacityrollover.js',
    'lib_highcharts.chart': 'common/js/jquery.plugins/highcharts/highcharts.js' ,
    'lib_jquery.jqgrid': 'common/js/jquery.plugins/jqgrid/js/jquery.jqGrid.min.js' ,
    'lib_jquery.jqgrid_v3_8_2': 'common/jquery/plugins/jqgrid/jqgrid_v3_8_2/js/jquery.jqGrid.min.js' ,
    'lib_jquery.jqgrid_v4_0_0': 'common/jquery/plugins/jqgrid/jqgrid_v4_0_0/js/jquery.jqGrid.min.js' ,
    'lib_jquery.jstree': 'common/js/jquery.plugins/jstree/jquery.jstree.js' ,
    'lib_grid.locale-es': 'common/js/jquery.plugins/jqgrid/js/i18n/grid.locale-es.js' ,
    'lib_jquery.carousel': 'common/js/jquery.plugins/jquerytool/js/jquery.tools.min.js' ,
    'lib_jquery.jcarousel': 'common/js/jquery.plugins/jcarousel/js/jquery.jcarousel.min.js' ,
    'lib_jwplayer_v5_8': 'common/jwplayer/jwplayer_v5_8/jwplayer.js' ,
    'lib_jwplayer_v5_6_1768': 'common/jwplayer/jwplayer_v5_6_1768/jwplayer.js' ,
    'lib_jwplayer_v5_1_854': 'common/jwplayer/jwplayer_v5_1_854/jwplayer.js' ,
    'lib_jquery.jquery.tablednd': 'common/jquery/plugins/jqgrid/jqgrid_v4_0_0/plugins/jquery.tablednd.js' ,
    'lib_jquery.jquery.contextmenu': 'common/jquery/plugins/jqgrid/jqgrid_v4_0_0/plugins/jquery.contextmenu.js' ,
    'lib_jquery.ui.multiselect': 'common/jquery/plugins/jqgrid/jqgrid_v4_0_0/plugins/ui.multiselect.js' ,
    'lib_languageswitch': 'atlcms/js/language.js' ,
    'lib_jquery.easypaginate': 'common/js/jquery.plugins/easypaginate/jquery.easypaginate.js' ,
    'lib_galleria': 'common/js/jquery.plugins/galleria/galleria-1.2.8.min.js' ,
    'lib_galleriffic': 'common/js/jquery.plugins/galleriffic/jquery.galleriffic.js' ,
    
    'lib_facebook_plugins': 'common/js/facebook.plugins/script.js' ,
}

__default_aspects_categories__ = (
    ('blocks', _('Bloks')),
    ('home', _('Home page')),
    ('sections', _('Site Sections')),
)

ASPECTS_CATEGORIES = getattr(settings, "ATLANTE_CMS_ASPECT_CATEGORY", __default_aspects_categories__)

## tipos de ficheros que se usan por defecto
#__file_types__ = (
#    ('PDF', 'PDF'),
#    ('XLS', 'XLS'),
#    ('DOC', 'DOC'),
#)
## si no se definen en el setting del projecto los tipos de ficheos a utilizar, se asignan los tipos predefinidos
#FILE_TYPES = getattr(settings, "ATLANTE_CMS_FILE_TYPES", __file_types__)
## se selecciona el primerero como el tipo de fichero por defecto
#__default_file_type__ = FILE_TYPES[0][0]
## si no se define en el setting del projecto el tipo de ficheo a utilizar por defecto, se escoge el primero de todos
#DEFAULT_FILE_TYPE = getattr(settings, "ATLANTE_CMS_DEFAULT_FILE_TYPE", __default_file_type__)
#
#__file_types_ext__ = ['.%s' %ft[1].lower() for ft in FILE_TYPES]


__file_types_ext__ = ['.pdf','.doc','.rtf','.txt','.xls','.csv']
# extensión de tipos de ficheros que se usan en el sitio
FILE_TYPES_EXT = getattr(settings, "ATLANTE_CMS_FILE_TYPES_EXT", __file_types_ext__)

__images_ext__ = ['.jpg','.jpeg','.gif','.png','.tif','.tiff']
# extensión de tipos de imágenes que se usan en el sitio
IMAGES_EXT = getattr(settings, "ATLANTE_CMS_IMAGES_EXT", __images_ext__)

FB_VERSIONS = getattr(settings, 'FILEBROWSER_VERSIONS', None)
#if FB_VERSIONS is not None:
#    THUMBNAIL

__audios_ext__ = ['.mp3','.mp4','.wav','.aiff','.midi','.m4p','.wma','.ogg']
# extensión de tipos de imágenes que se usan en el sitio
AUDIOS_EXT = getattr(settings, "ATLANTE_CMS_AUDIOS_EXT", __audios_ext__)


RESOURCES_CHOICES = (
    ('Image', _('Image')),
    ('Flash', 'Flash'),
)
DEFAULT_RESOURCE = RESOURCES_CHOICES[0][0]

VIDEO_SOURCES_CHOICES = (
    ('local', _('Local file')),
    ('ftp', _('FTP Folder')),
    ('external', _('External URL')),
    ('embeded', _('Embeded video')),
)

DEFAULT_VIDEO_SOURCE = VIDEO_SOURCES_CHOICES[0][0]

default_video_settings = {
     'audio_freq': 22050,
     'audio_bitrate': 128,
     'video_size': '440x328',
     'video_bitrate': 800,  
}
if hasattr(settings, "ATLANTE_CMS_VIDEO_SETTINGS"):
    VIDEO_SETTINGS = getattr(settings, "ATLANTE_CMS_VIDEO_SETTINGS")
    for key, value in default_video_settings.items():
        exist_value = VIDEO_SETTINGS.get(key, False)
        if not exist_value:
            VIDEO_SETTINGS[key]=value
else:
    VIDEO_SETTINGS = default_video_settings
    
STATE_CHOICES=(
    ('Public', _('Public')),
    ('Private', _('Private'))
)

DEFAULT_STATE=STATE_CHOICES[0][0]

ALLOW_COMMENT_CHOICES=(
    (0, _('No, don\'t allow comments.')),
    (1, _('Allow comments to be added automatically.')),
    (2, _('Yes, allow comments after I approve them.')),
)

DEFAULT_COMMENT_CHOICES=ALLOW_COMMENT_CHOICES[2][0]

DEFAULT_USER_PROFILE_FOLDERS = ['images', 'desktop', 'videos', 'noticias', 'documents', 'others']
USER_PROFILE_FOLDERS = getattr(settings, 'ATLANTE_CMS_USER_PROFILE_FOLDERS', DEFAULT_USER_PROFILE_FOLDERS)


# default images size
image_size = (640, 480)
# default thumbnail size and the crop option
thumbnail_size = (100, 100, True)
IMAGE_SIZE = getattr(settings, "IMAGE_SIZE", image_size)
THUMBNAIL_SIZE = getattr(settings, "IMAGE_SIZE", thumbnail_size)

