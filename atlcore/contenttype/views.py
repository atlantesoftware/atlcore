# Create your views here.
# -*- coding: utf-8 -*-
from django.template.context import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from atlcore.contenttype.models import Folder, Node
from atlcore.site.dublincore import DublinCore


def details_view(request, id=None, slug=None, view_name=None):
    atl_node = Node.objects.get(id=id).get_instance()
    dc = DublinCore()
    dc.title = atl_node.title
    dc.description = atl_node.meta_description
    dc.keywords = atl_node.subject
    dc.author = atl_node.creator
    dc.copyright = atl_node.rights
    context = {}
    context['atl_node'] = atl_node
    context['dc'] = dc
    if not view_name:
        template = 'atlcontenttype/%s.html' % context['atl_node'].class_name_instance
    return render_to_response(template,
        context,
        context_instance=RequestContext(request))
