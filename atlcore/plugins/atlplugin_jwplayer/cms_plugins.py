#coding=UTF-8
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from atlcore.plugins.atlplugin_jwplayer.models import AtlJWPlayer

class AtlJWPlayerBoxPlugin(CMSPluginBase):
    model = AtlJWPlayer # Model where data about this plugin is saved
    name = _("ATlJWPlayerBox Plugin") # Name of the plugin
    render_template = "atlplugin_jwplayer/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):

        context.update({'instance':instance})
        return context

plugin_pool.register_plugin(AtlJWPlayerBoxPlugin) # register the plugin
