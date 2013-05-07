from atlcore.relations import settings as relsettings

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
from django.utils import translation

def Q():
    apps = relsettings.ALLOWEDS_APPS
    q = []    
    f = None
    for conf in apps:
        app = conf['app']
        if conf.has_key('models'):
            mdls = [model_conf['model'] for model_conf in conf['models']]
            if f is not None:
                f = f | models.Q(app_label = a, model__in = mdls)
            else:
                f = models.Q(app_label = app, model__in = mdls)                            
        else:
            if f is not None:
                f = f | models.Q(app_label = app)
            else:
                f = models.Q(app_label = app)
    return f

def get_list(models_name, q):
    
    def append_obj(ct, objects, field='title'):
        cur_language = translation.get_language()
        objs = ct.model_class().objects.filter(**{'%s__contains' %field: q}).filter(language = cur_language)
        for obj in objs:
            field_val = getattr(obj, field, '')
            if field_val is not None:
                objects.append({
                    'id':u'ct_%s_obj_%s'% (ct.id, obj.id),
                    'label':'%s (%s)' %(field_val, _(obj._meta.module_name)),
                    'value':field_val,
                }) 
    
    apps = relsettings.ALLOWEDS_APPS
    objects = []
    full_apps = []
    for conf in apps:
        app = conf['app']
        text = 'title'
        if conf.has_key('models'):
            for model_conf in conf['models']:
                model_name = model_conf['model']
                if model_name in models_name:
                    models_name.remove(model_name)
                    cts = ContentType.objects.filter(app_label=app, model=model_name)
                    for ct in cts:
                        fields = model_conf['fields']
                        if fields:
                            for field in fields:
                                append_obj(ct, objects, field)
                        else:
                            append_obj(ct, objects)
        else:
            full_apps.append(app)
    for app in full_apps:
        cts = ContentType.objects.filter(app_label=app)
        for ct in cts:
            if ct.model in models_name:
                models_name.remove(ct.model)              
                append_obj(ct, objects)
    return objects 