'''
Created on 15/09/2010

@author: ariel
'''
from django import template
from atlcore.settings import MEDIA_URL as ATL_MEDIA_URL
from django.conf import settings

register = template.Library()

@register.inclusion_tag('vcl/component.html')
def show_component(component, template_name=None):
    if template_name and template_name in component.template.keys(): 
        template = component.template[template_name]
    else:
        template = component.template['default']
    return {
        'component': component,
        'template': template,
        'view_type': template_name,
        'template_name': template_name,
        'MEDIA_URL': settings.MEDIA_URL,
        'ATL_MEDIA_URL': ATL_MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL
    }
