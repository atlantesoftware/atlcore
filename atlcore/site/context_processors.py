#encoding=UTF-8
from django.conf import settings
from django.utils.translation import get_language
from atlcore.siteprofile.models import SiteProfile
from atlcore.site.dublincore import DublinCore


def common(request):
# *** Se ha comentado este código porque en lo adelante la clase Site ***  
# *** tendrá una propiedad skin con el valor correspondiente          ***
    try:
        skin = SiteProfile.objects.get(id=settings.SITE_ID).skin
    except:
        skin = None
    site_profile = SiteProfile.objects.get(site__id=settings.SITE_ID)
    context = {}
#    context['SKIN_STATIC_URL'] = '%sskins/%s/' % (settings.STATIC_URL, site_profile.skin.slug)

    dc = DublinCore()
    dc.title = site_profile.site.name
    dc.description = site_profile.description
    dc.keywords = site_profile.keywords
    context['dc'] = dc
    context['DEBUG'] =  settings.DEBUG
    context['site'] = settings.SITE_ID
    context['site_profile'] = site_profile
    context['LANGUAGE'] = get_language()
    return context