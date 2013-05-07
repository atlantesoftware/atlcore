##coding=UTF-8
#from atlcore.permissions.models import AtlUserProfile
#
#from django.contrib.admin import ModelAdmin, site
#from django.conf import settings
#
#use_tinymce = False
#if 'tinymce' in settings.INSTALLED_APPS:
#    from tinymce.widgets import TinyMCE
#    use_tinymce = True
#
#class AtlUserProfileAdmin(ModelAdmin):
#
#    def formfield_for_dbfield(self, db_field, **kwargs):
#        if use_tinymce and (db_field.name == 'biography'):
#            return db_field.formfield(widget=TinyMCE(attrs={'cols': 100, 'rows': 40},))
#        return super(AtlUserProfileAdmin, self).formfield_for_dbfield(db_field, **kwargs)
#
#site.register(AtlUserProfile, AtlUserProfileAdmin)