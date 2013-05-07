#coding=UTF-8
"""
AtlanteSoftware diciembre 2012
"""

from django.contrib import admin
from django.utils.translation import ugettext as _

from atlcore.contenttype.models import News, Video, Folder, Audio, Banner, \
                                       Document, File, Link, Map, Picture
from atlcore.contenttype.admin.widgets import LinkContentInput
from tinymce.widgets import TinyMCE
from atlcore.contenttype.admin.base import Base


use_tinymce = True


class FolderAdmin(Base):
    fieldsets = [
        (_('Main information'), 
         {'fields': ['title', 'slug', 'image', 'description','date', \
                     'aspect', 'parent', 'sites', 'state', 'original_aspect']}),
        (_('Metadata'), 
         {'fields': ['creator', 'owner', 'contributor', 'language', 'neutral',\
                     'format', 'publisher', 'rights', 'type', 'subject'], \
          'classes': ['collapse']}),
    ]
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(FolderAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if use_tinymce and db_field.name == 'description':
            return db_field.formfield(widget=TinyMCE(attrs={'cols': 100, 'rows': 10},))
        return field


class NewsAdmin(Base):
    fieldsets = [
        (_('Main information'), {'fields': ['title', 'slug', 'description', 'body', 'image', 'parent', 'aspect', 'original_aspect', 'sites', 'state', 'author_photo', 'date']}),
        #(_('Interactivity options'), {'fields':['allow_comment', 'allow_voting'], 'classes': ['collapse']}),
        (_('Metadata'), {'fields': ['creator', 'owner', 'contributor', 'language', 'neutral', 'format', 'publisher', 'rights', 'type', 'subject', 'meta_description'], 'classes': ['collapse']}),
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(NewsAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if use_tinymce and (db_field.name == 'body' or db_field.name == 'description'):
            return db_field.formfield(widget=TinyMCE(attrs={'cols': 100, 'rows': 40},))
        return field


class VideoAdmin(Base):
    fieldsets = [
        (_('Main information'), {'fields': ['title', 'slug', 'description','body', 'video_source', 'video', 'video_url', 'external_url', 'embeded_video', 'thumbnail', 'x_aspect_ratio', 'y_aspect_ratio', 'parent', 'aspect', 'original_aspect']}),
        (_('Metadata'), {'fields': ['creator', 'contributor', 'owner', 'language', 'neutral', 'format', 'publisher', 'rights', 'type', 'subject'], 'classes': ['collapse']}),
    ] 
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(VideoAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if use_tinymce and (db_field.name == 'body' or db_field.name == 'description'):
            return db_field.formfield(widget=TinyMCE(attrs={'cols': 100, 'rows': 40},))
        return field



class AudioAdmin(Base):
    fieldsets = [
        (_('Main information'), {'fields': ['title', 'slug', 'image', 'description', 'parent', 'aspect', 'original_aspect', 'mp3_file', 'ogg_file', 'wav_file','owner']}),
    ]
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(AudioAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        return field


class BannerAdmin(Base):
    fieldsets = [
        (_('Main information'), {'fields': ['title', 'slug', 'image', 'open_in_new_page', 'url', 'width', 'height', 'description', 'parent', 'aspect', 'original_aspect', 'sites', 'state']}),
        #(_('Interactivity options'), {'fields':['allow_comment', 'allow_voting'], 'classes': ['collapse']}),
        (_('Metadata'), {'fields': ['creator', 'contributor', 'owner', 'language', 'neutral', 'format', 'publisher', 'rights', 'type', 'subject'], 'classes': ['collapse']}),
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(BannerAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if use_tinymce and (db_field.name == 'description'):
            return db_field.formfield(widget=TinyMCE(attrs={'cols': 100, 'rows': 40},))
        if db_field.name == "url":
            return db_field.formfield(widget=LinkContentInput())
        return field

class DocumentAdmin(Base):
    fieldsets = [
        (_('Main information'), {'fields': ['title', 'slug', 'description', 'body', 'image', 'aspect', 'original_aspect', 'sites', 'state', 'parent']}),
        #(_('Interactivity options'), {'fields':['allow_comment', 'allow_voting'], 'classes': ['collapse']}),
        (_('Metadata'), {'fields': ['creator', 'owner', 'contributor', 'language', 'neutral', 'format', 'publisher', 'rights', 'type', 'subject'], 'classes': ['collapse']}),
    ]    

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(DocumentAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if use_tinymce and (db_field.name == 'body' or db_field.name == 'description'):
            return db_field.formfield(widget=TinyMCE(attrs={'cols': 100, 'rows': 40},))
        return field

class FileAdmin(Base):
    fieldsets = [
        (_('Main information'), {'fields': ['title', 'slug', 'image','file', 'description', 'parent', 'aspect', 'original_aspect', 'sites', 'state']}),
        #(_('Interactivity options'), {'fields':['allow_comment', 'allow_voting'], 'classes': ['collapse']}),
        (_('Metadata'), {'fields': ['creator', 'contributor', 'owner', 'language', 'neutral', 'format', 'publisher', 'rights', 'type', 'subject'], 'classes': ['collapse']}),
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(FileAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if use_tinymce and (db_field.name == 'description'):
            return db_field.formfield(widget=TinyMCE(attrs={'cols': 100, 'rows': 40},))
        return field

class PictureAdmin(Base):
    fieldsets = [
        (_('Main information'), {'fields': ['title', 'slug', 'image', 'description', 'parent', 'aspect', 'original_aspect', 'sites', 'state']}),
        #(_('Interactivity options'), {'fields':['allow_comment', 'allow_voting'], 'classes': ['collapse']}),
        (_('Metadata'), {'fields': ['creator', 'contributor', 'owner', 'language', 'neutral', 'format', 'publisher', 'rights', 'type', 'subject'], 'classes': ['collapse']}),
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(PictureAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if use_tinymce and (db_field.name == 'description'):
            return db_field.formfield(widget=TinyMCE(attrs={'cols': 100, 'rows': 40},))
        return field

class LinkAdmin(Base):
    fieldsets = [
        (_('Main information'), {'fields': ['title', 'slug', 'url', 'open_in_new_page', 'description', 'image', 'icon', 'aspect', 'original_aspect',  'sites', 'parent', 'state']}),
        #(_('Interactivity options'), {'fields':['allow_comment', 'allow_voting'], 'classes': ['collapse']}),
        (_('Metadata'), {'fields': ['creator', 'contributor', 'owner', 'language', 'neutral', 'format', 'publisher', 'rights', 'type', 'subject'], 'classes': ['collapse']}),
    ]    

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(LinkAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if use_tinymce and (db_field.name == 'body' or db_field.name == 'description'):
            return db_field.formfield(widget=TinyMCE(attrs={'cols': 100, 'rows': 10},))
        if db_field.name == "url":
            return db_field.formfield(widget=LinkContentInput())
        return field

class MapAdmin(Base):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(MapAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        return field



admin.site.register(Folder, FolderAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Map, MapAdmin)

Folder.register(Folder)
Folder.register(Video)
Folder.register(News)
Folder.register(Audio)
Folder.register(Banner)
Folder.register(Document)
Folder.register(File)
Folder.register(Picture)
Folder.register(Link)
Folder.register(Map)


