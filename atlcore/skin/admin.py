#coding=UTF-8
from models import Skin, SkinType
from atlcore.skin.tools import py2xml, xml2py

from django import forms
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied, MultipleObjectsReturned, ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

csrf_protect_m = method_decorator(csrf_protect)

def deserialize( xmlString ):
    deserializer = xml2py.XML2Py()
    return deserializer.parse( xmlString )

def serialize( pyObject, root=None ) :
    serializer = py2xml.Py2XML()
    return serializer.parse( pyObject, root )

def xml2form(skin):
    xml = render_to_string('%s/skin_form.xml' %skin)
    dic = deserialize(xml)
    fields = {}
    if dic:
        dic = dic['skin-form']
        print dic
        if isinstance(dic, list):
            for field in dic:
                field_type = field.get('type', None)
                field_name = field_prop.get('name', None)
                field_value = field_prop.get('value', None)
                if field_type is not None and field_name is not None:
                    if field_type == 'CharField':
                        fields[field_name] = forms.CharField(initial=field_value)
    DynamicForm = type('DynamicForm', (forms.Form,), fields)
    print DynamicForm
    return

class SkinAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.module_name
        urls = super(SkinAdmin, self).get_urls()
        my_urls = patterns('',        
            url(r'^(?P<id>\d+)/customize/$', self.admin_site.admin_view(self.customize), name='%s_%s_change' % info),
        )
        return my_urls + urls
    
    @csrf_protect_m
    def customize(self, request, id):
        try:
            skin = self.model.objects.get(pk=id)
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            raise Http404()
        form = xml2form(skin.slug)
        return HttpResponse('%s'%id)

class SkinTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Skin, SkinAdmin)
admin.site.register(SkinType, SkinTypeAdmin)