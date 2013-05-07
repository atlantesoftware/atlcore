#coding=UTF-8
import atlcore.settings as atlsettings
#from atlcms.atl_content_type.admin.clipboard import Clipboard
from django.conf import settings
from django.utils.translation import get_language
from atlcore.contenttype.models import Container
from atlcore.site.mediaenvironment import MediaEnvironment


def get_server_url(request):
    url = request.build_absolute_uri()
    path = request.get_full_path()
    pos = url.rindex(path)
    return url[:pos]

def get_server_name(request):
    url = get_server_url(request)
    pos = url.find('//')
    return url[pos+2:]

def admin_var(request):
    tmp = request.path.split('/')
    prefix = ''
    if tmp:
        if tmp[0] != '':
            prefix = tmp[0]
        elif len(tmp) > 1:
            prefix = tmp[1]     
    if prefix == atlsettings.ADMIN_PREFIX:
        from atlcore.cms.admin import panel
        context = panel.__atl_models_dic__(request)
        #context['root_path'] = panel.root_path
#        context['can_paste_from_clipboard'] = Clipboard.can_paste(request)
        return context
    return {}

def common(request):
    admin_dic = admin_var(request)
    context = {
        'ATL_MEDIA_URL': atlsettings.MEDIA_URL,
        'SITE_ID': settings.SITE_ID, 
        'MEDIA_URL': settings.MEDIA_URL,
        'DEBUG' : settings.DEBUG, 
        'SERVER_URL':get_server_url(request),
        'SERVER_NAME':get_server_name(request),
        'LANGUAGE_CODE':settings.LANGUAGE_CODE,
        'LANGUAGES':atlsettings.LANGUAGES,
        'LANGUAGE': get_language(),
        'IP_ADDR':request.META['REMOTE_ADDR'],
        'USER':request.user,
        'USE_COMMENTS': 'django.contrib.comments' in settings.INSTALLED_APPS,
    }
    context.update(admin_dic)
    return context