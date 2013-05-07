#coding=UTF-8
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from atlcore.contenttype.models import News as NewsContenttype
from atlcore.plugins.news.models import News
from atlcore.plugins.news.models import NewsList as NewsListModel


class NewsPlugin(CMSPluginBase):
    model = News # Model where data about this plugin is saved
    name = _("AtlNews Plugin") # Name of the plugin
    render_template = "atlplugin_news/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

class NewsListPlugin(CMSPluginBase):
    model = NewsListModel # Model where data about this plugin is saved
    name = _("AtlNewsList Plugin") # Name of the plugin
    render_template = "atlplugin_newslist/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        context['news_list'] = NewsContenttype.objects.filter(state='Public').order_by('-order')[:instance.amount]
        return context



plugin_pool.register_plugin(NewsPlugin) # register the plugin
plugin_pool.register_plugin(NewsListPlugin) # register the plugin
