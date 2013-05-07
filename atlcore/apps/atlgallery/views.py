# -*- coding: utf-8 -*-
__author__ = 'hailem'

from django.template.context import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from atlcore.contenttype.models import Folder


def image_list_view(request, id=None, slug=None, view_name=None):
    context = {}
    context['gallery'] = Folder.objects.get(id=id)
    return render_to_response('atlgallery/gallery.html',
        context,
        context_instance=RequestContext(request))