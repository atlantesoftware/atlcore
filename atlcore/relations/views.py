#coding=UTF-8
from atlcore.relations import helper

from django.http import HttpResponse
from django.utils import simplejson
from django.utils.translation import ugettext as _


def json_objects(request, model_list):
    q = request.GET.get('term', None)
    objects = []
    models_name = model_list.split(',')
    if q:
        objects = helper.get_list(models_name, q)  
    return HttpResponse(simplejson.dumps(objects), mimetype='application/json')
