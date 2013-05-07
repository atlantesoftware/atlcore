#coding=UTF-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from atlgallery.models import AtlGallery as AtlGalleryModel
from django.utils.translation import ugettext as _

class AtlGalleryPlugin(CMSPluginBase):
    model = AtlGalleryModel # Model where data about this plugin is saved
    name = _("AtlGallery Plugin") # Name of the plugin
    render_template = "atlgallery/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

plugin_pool.register_plugin(AtlGalleryPlugin) # register the plugin

#TODO: Hacer que en las galerías se introduzca la página (django-cms) que se usará para mostrar las fotos por separado