#coding=UTF-8
from atlcore.contenttype import helper

from django import template

register = template.Library()

@register.filter(name='can_add')
def can_add(object, user):
    return helper.check_permission(user, 'add', object)

@register.filter(name='can_delete')
def can_delete(object, user):
    return helper.check_permission(user, 'delete', object)

@register.filter(name='can_change')
def can_change(object, user):
    return helper.check_permission(user, 'change', object)

@register.filter(name='can_read')
def can_read(object, user):
    return helper.check_permission(user, 'read', object)