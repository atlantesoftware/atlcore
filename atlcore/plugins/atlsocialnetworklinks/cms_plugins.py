#coding=UTF-8
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from atlcore.contenttype.models import News
from atlcore.plugins.atlsocialnetworklinks.models import SocialNetworkLinks
from news_box.models import NewsListBox as NewsListBoxModel
from django.utils.translation import ugettext as _

class SocialNetworkLinksPlugin(CMSPluginBase):
    model = SocialNetworkLinks # Model where data about this plugin is saved
    name = _("NewsBox Plugin") # Name of the plugin
    render_template = "news_box/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context



plugin_pool.register_plugin(NewsBoxPlugin) # register the plugin
