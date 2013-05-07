#coding=UTF-8
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from atlcore.plugins.document.models import Document

class DocumentPlugin(CMSPluginBase):
    model = Document # Model where data about this plugin is saved
    name = _("AtlDocument Plugin") # Name of the plugin
    render_template = "atlplugin_document/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context


plugin_pool.register_plugin(DocumentPlugin) # register the plugin
