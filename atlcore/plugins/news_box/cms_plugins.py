#coding=UTF-8
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from atlcore.contenttype.models import News
from atlcore.plugins.news_box.models import NewsBox as NewsBoxModel
from atlcore.plugins.news_box.models import NewsListBox as NewsListBoxModel

class NewsBoxPlugin(CMSPluginBase):
    model = NewsBoxModel # Model where data about this plugin is saved
    name = _("NewsBox Plugin") # Name of the plugin
    render_template = "news_box/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        return context

class NewsListBoxPlugin(CMSPluginBase):
    model = NewsListBoxModel # Model where data about this plugin is saved
    name = _("NewsListBox Plugin") # Name of the plugin
    render_template = "news_list_box/plugin.html" # template to render the plugin with

    def render(self, context, instance, placeholder):
        context.update({'instance':instance})
        print 'Cantidad de noticias -> %s' % instance.max_element
        context['news_list'] = News.objects.filter(state='Public').order_by('-order')[:instance.max_element]
        return context


plugin_pool.register_plugin(NewsBoxPlugin) # register the plugin
plugin_pool.register_plugin(NewsListBoxPlugin) # register the plugin