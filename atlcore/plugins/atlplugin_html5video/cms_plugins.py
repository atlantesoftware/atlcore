# -*- coding: utf-8 -*-

import os

from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from atlcore.plugins.atlplugin_html5video.models import HTML5Video

class HTML5VideoPlugin(CMSPluginBase):
    model = HTML5Video
    name = _("Atlantesoftware HTML5 Video")

    render_template = "atlplugin_html5video/video.html"
    text_enabled = True

    general_fields = [
        'title',
        ('width', 'height'),
        'auto_play',
        'auto_hide',
        'fullscreen',
        'loop',
        ]

    fieldsets = [
        (None, {
            'fields': general_fields,
        }),
        (_('formats'), {
            'fields': ('video',)
        })
    ]

    def render(self, context, instance, placeholder):
        formats = {}
#        for format in ('video_mp4', 'video_webm', 'video_ogv'):
#            if getattr(instance, format + '_id'):
#                formats[format.replace('_', '/')] = getattr(instance, format).url
        context.update({
            'object': instance,
            'placeholder':placeholder,
            'formats': formats
        })
        return context

    def icon_src(self, instance):
#        Todo: Hacer que este método funcione
        return os.path.normpath(u"%s/icons/video_%sx%s.png" % ('cambiar aquí el path', 32, 32,))

plugin_pool.register_plugin(HTML5VideoPlugin)