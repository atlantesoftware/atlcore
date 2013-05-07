#coding=UTF-8
from models import SiteProfile 

from django.contrib import admin

class SiteProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(SiteProfile, SiteProfileAdmin)