from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _, get_language

import atlcore.settings as atlsettings

register = template.Library()

def lang_flag_url(name):
    media_url = atlsettings.MEDIA_URL
    name = name.lower().strip()
    return u'/static/common/flags/languages/%s.gif' %name[:2]
lang_flag_url = stringfilter(lang_flag_url)
register.filter('lang_flag_url', lang_flag_url)
