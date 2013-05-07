# -*- coding: utf-8 -*-
from django.template.context import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from atlcore.contenttype.models import Folder, Node


def details_view(request, id=None, slug=None, view_name=None):
    context = {}
    context['atl_node'] = Node.objects.get(id=id).get_instance()
    return render_to_response('mysite/news.html',
                              context,
                              context_instance=RequestContext(request))
