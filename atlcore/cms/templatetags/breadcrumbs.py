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

@register.filter(name='breadcrumbs')
def breadcrumbs(object, title=None):
    html = mark_safe('<a href="%s">%s</a>' %(reverse('admin:index'), _('Home')))
    if object:
        objects = object.get_ancestors()
        for obj in objects:
            html += mark_safe(' &rsaquo;  <a href="%s">%s</a>' %(obj.admin_url(), obj.title))
        if title is not None:
            html += mark_safe(' &rsaquo;  <a href="%s">%s</a>' %(object.admin_url(), object.title))
            html += mark_safe(' &rsaquo;  %s' %title)
        else:
            html += mark_safe(' &rsaquo; %s' %(object.title))
    else:
        html += mark_safe(' &rsaquo;  %s' %title)
    return html

@register.filter(name='breadcrumbs_for_model')
def breadcrumbs_for_model(object):
    html = mark_safe('<a href="%s">%s</a>' %(reverse('admin:index'), _('Home')))
    if object:
        objects = object.get_ancestors()
        for obj in objects:
            html += mark_safe(' &rsaquo;  <a href="%s">%s</a>' %(obj.admin_url(), obj.title))
        try:
            plural_name = object._meta.object_name_plural
        except:
            plural_name = '%s' %object._meta.object_name 
        html += mark_safe(' &rsaquo;  <a href="%s">%ss</a>' %(object.admin_model_url(), plural_name))
        title = _('Objects list')
        html += mark_safe(' &rsaquo;  %s' %title)
    return html