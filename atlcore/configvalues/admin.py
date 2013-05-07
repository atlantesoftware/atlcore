#coding=UTF-8
from django.contrib import admin
from configvalues.models import ConfigValues

class ConfigValuesAdmin(admin.ModelAdmin):
    pass
    

admin.site.register(ConfigValues, ConfigValuesAdmin)    