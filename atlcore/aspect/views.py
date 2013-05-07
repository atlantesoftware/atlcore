#coding=UTF-8
from atlcore.aspect.models import Aspect

from django.http import HttpResponse
from django.utils import simplejson

def list_aspect(request, parent_id=0):
    try:
        if parent_id == u'0':
            aspects = Aspect.objects.filter(parent=None)
        else:
            aspects = Aspect.objects.filter(parent=parent_id)
    except:
        aspects = Aspect.objects.none()
    tree = []
    for aspect in aspects:
        node = {
            'data': aspect.title,
            'attr': {'id': 'node_%d'%aspect.id},
            'state': 'closed',
            'children' :[],
        }
        tree.append(node)
    return HttpResponse(simplejson.dumps(tree), mimetype='application/json')
