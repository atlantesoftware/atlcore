#coding=UTF-8
#from atlante_cms.atl_aspect.models import Aspect
#from atlante_cms.atl_content_type.models import AtlContainer
#from atlante_cms.context_processors import get_server_url
from django.http import Http404

from django.conf.urls.defaults import patterns, url, include
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils import feedgenerator
from django.conf import settings
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.contrib.syndication.views import Feed

from atlcore.site.dublincore import DublinCore
from atlcore.site.mediaenvironment import MediaEnvironment
from atlcore.contenttype.models import Container, Node
from atlcore.vcl.components import Content as Content_Component
from atlcore.vcl.components import Container as Container_Component
from atlcore.vcl.components import JWPlayer
from atlcore.vcl.components.galleria import Galleria

class BasePage(object):
    
    details_template = None
    list_template = None    
    
    def __init__(self, model, atl_site):
        self.model = model
        self.opts = model._meta
        self.atl_site = atl_site
        self.media_environment = MediaEnvironment()
        super(BasePage, self).__init__()
    
    def get_urls(self):
        urlpatterns = patterns('',
#            url(r'^$', self.base_view, name='%s_base' %self.opts.module_name),
#            url(r'^list/$', self.list_view, name='%s_list' %self.opts.module_name),
#            url(r'^summaries/$', self.list_view, {'template_name':'summaries'}, name='%s_summaries' %self.opts.module_name),            
#            url(r'^list/(?P<aspect_slug>.+)/$', self.list_view, name='%s_aspect_list' %self.opts.module_name),
#            url(r'^summaries/(?P<aspect_slug>.+)/$', self.list_view, {'template_name':'summaries'}, name='%s_aspect_summaries' %self.opts.module_name),           
            url(r'^(?P<id>[a-fA-F0-9]{32})/$', self.details_view, name='%s_details1' %self.opts.module_name),
            url(r'^(?P<slug>[a-zA-Z0-9-]+)/$', self.details_view, name='%s_details1' %self.opts.module_name),
            url(r'^(?P<id>[a-fA-F0-9]{32})/(?P<slug>[a-zA-Z0-9-]+)/$', self.details_view, name='%s_details' %self.opts.module_name),
            url(r'^(?P<id>[a-fA-F0-9]{32})/(?P<slug>[a-zA-Z0-9-]+)/(?P<template_name>.+)/$', self.details_view, name='%s_details_with_view' %self.opts.module_name),
#            url(r'^(?P<id>\d+)/(?P<slug>.+)/$', self.details_view, name='%s_slug_details' %self.opts.module_name),
#            url(r'^(?P<aspect_slug>.+)/$', self.list_view, name='%s_aspect_base' %self.opts.module_name),
            url(r'^ajax/(?P<id>[a-fA-F0-9]{32})/(?P<view_name>.+)/$', self.ajax_details_view, name='%s_ajax_details' %self.opts.module_name),
        )
        return urlpatterns
    
    @classmethod
    def get_metadata_from_content(self, content):
        '''
        Construye una instancia de la clase DublinCore dándole como propiedades, la información del contenido
        '''
        dc = DublinCore()
        
        dc.title = content.title
        if content.meta_description:
            dc.description = content.meta_description
        else:
            dc.description = content.description
        dc.keywords = content.subject
        return dc

        
    def get_base_context(self, request, content):
        content.create_relation_methods()
        context = self.atl_site.get_base_context(request)
        context['dc'] = self.get_metadata_from_content(content)
        context['content'] = content
        return context

    def details_view(self, request, id=None, extra_context=None, slug=None, template_name='details'):
        if id:            
            content = self.model.objects.get(pk=id)
        else:
            content = self.model.objects.get(slug=slug)
        
        if content:            
            content.viewed()            
        
        context = self.get_base_context(request, content)
        context['content_component'] = Content_Component(content)
        context['media_environment'].append_media(context['content_component'])
        context.update(extra_context or {})
        return context
    
    def ajax_details_view(self, request, id, view_name):
        pass
    
class ContentPage(BasePage):
    
    def details_view(self, request, id=None, extra_context=None, slug=None, template_name='details'):
        context = super(ContentPage, self).details_view(request, id, extra_context, slug, template_name)
        context['template_name'] = template_name
        template_list = [
            'site/%s/%s.html' %(self.opts.module_name, template_name),
            'site/content_%s.html' % (template_name),
            'site/content.html',
        ]
        return render_to_response(self.details_template or template_list, context, context_instance=RequestContext(request))
    
    def ajax_details_view(self, request, id, view_name='details'):
        pass
    
class ContainerFeed(Feed):
    feed_type = feedgenerator.Rss201rev2Feed
    
    def get_object(self, request, id, slug=None):
        return get_object_or_404(Node, pk=id)
    
    def title(self, obj):
        return obj.title
    
    def link(self, obj):
        return 'link'
    
    def description(self, obj):
        return obj.description
    
    def items(self, obj):
        return [node.get_instance() for node in Node.objects.filter(parent__pk=obj.id).order_by('-date')[:10]]
    
    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_author_name(self, item):
        return item.creator
    
    def item_pubdate(self, item):
        return item.date
    
        
class ContainerPage(BasePage):
    
    def _get_paginator(self, content, request):
        paginator = Paginator(content.get_childrens(order="-date"), getattr(settings, 'PAGINATOR_MAX_ITEMS', 8))
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1
        try:
            return paginator.page(page)
        except (EmptyPage, InvalidPage):
            return paginator.page(paginator.num_pages)
        
    def get_urls(self):
        urlpatterns = patterns('', 
                               url(r'^(?P<id>[a-fA-F0-9]{32})/rss/$', ContainerFeed(), name='%s_rss_slug' %self.opts.module_name),
                               url(r'^(?P<id>[a-fA-F0-9]{32})/(?P<slug>[a-zA-Z0-9-]+)/rss/$', ContainerFeed(), name='%s_rss' %self.opts.module_name))
        urlpatterns += super(ContainerPage, self).get_urls() 
        return urlpatterns
        
    def details_view(self, request, id=None, extra_context=None, slug=None, template_name='details'):
        context = super(ContainerPage, self).details_view(request, id, extra_context, slug, template_name)
        context['content'].paginated_childrens = self._get_paginator(context['content'], request)
        if template_name == "gallery":
            from atlcore.vcl.components.galleriffic import Galleriffic
            #context['gallery_component'] = Galleria(context['content'].get_childrens())
            context['gallery_component'] = Galleriffic(context['content'].get_childrens())
            context['gallery_component'].id = 'gallery'
            context['gallery_component'].title = context['content'].title
            context['gallery_component'].description = context['content'].description
            context['media_environment'].append_media(context['gallery_component'])
        context['template_name'] = template_name
        context['content_component']._template['thumbnails'] = 'vcl/content/container_thumbnails.html'
        context['content_component']._template['gallery_items'] = 'vcl/content/container_gallery_items.html'
        context['content_component']._template['gallery'] = 'vcl/content/container_gallery.html'
        context['content_component']._template['list'] = 'vcl/content/container_list.html'
        template_list = [
            'site/%s/%s.html' %(self.opts.module_name, template_name),
            'site/container_%s.html' % (template_name),
            'site/container.html',
        ]
        return render_to_response(self.details_template or template_list, context, context_instance=RequestContext(request))

    def ajax_details_view(self, request, id, view_name='details'):
        page = int(request.GET.get('page', '1'))
        size =int(request.GET.get('size', '10'))       
        
        list = Node.objects.filter(parent__id = id)
        paginator = Paginator(list, size)        
        list_paginated = paginator.page(page)
        
        #context = self.get_base_context(request, content)
        context = {}
        context['template_name'] = view_name
        context['content_component'] = Container_Component(list_paginated.object_list)
        context['media_environment'] = MediaEnvironment()
        context['media_environment'].append_media(context['content_component'])
        
        return render_to_response('vcl/content/content_ajax.html', context, context_instance=RequestContext(request))
    

class VideoPage(BasePage):
    
    def details_view(self, request, id=None, extra_context=None, slug=None, template_name='details'):
        content = self.model.objects.get(pk=id).get_instance()
        context = self.get_base_context(request, content)
        context['video_player'] = JWPlayer(content)
        context['video_player'].id = 'PrincipalPlayer'
        if content.thumbnail: 
            context['video_player'].image = '%s%s' % (settings.STATIC_URL, content.thumbnail.url)
            print context['video_player'].image
        context['content_component'] = Content_Component(content)
        context['content_component'].video_player = context['video_player']
        context['template_name'] = template_name
        context['media_environment'].append_media(context['video_player'])
        context.update(extra_context or {})
        template_list = [
            'site/%s/%s.html' %(self.opts.module_name, template_name),
            'site/content_%s.html' %( template_name),
            'site/content.html',
        ]
        return render_to_response(self.details_template or template_list, context, context_instance=RequestContext(request))

