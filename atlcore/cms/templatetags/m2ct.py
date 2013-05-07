#coding=UTF-8
from django import template

register = template.Library()

@register.filter(name='get_meta')
def get_meta(object, attr=None):
    if attr is None:
        return object._meta
    return getattr(object._meta, attr, None)

@register.filter(name='checked')
def checked(key, d):
    return d.has_key(key)
