#coding=UTF-8
from atlcore.contenttype.models import Node

from django.contrib.admin.util import NestedObjects
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

session_key = 'atl_object_list'

def get_objects(request, key):
    items = []
    keys = request.POST.getlist(key)
    for k in keys:
        values = k.split('__')
        app_label = values[0]
        model_name = values[1]
        id = values[2]
        try:
            ct = ContentType.objects.get(app_label=app_label, model=model_name)
            obj = ct.get_object_for_this_type(pk=id)
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            pass
        else:
            if obj:
                items.append(obj)
    #items.sort(key=lambda a: getattr(a, 'order'), reverse=True)
    return items

def get_deleted_objects(collection, user):
    collector = NestedObjects()
    for obj in collection:
        # TODO using a private model API!
        obj._collect_sub_objects(collector)
    objects = []
    perms_needed = False
    for key in collector.seen.keys():
        obj = collector.seen[key]
        opts = obj._meta
        if not user.has_perm('%s.delete_%s'%(opts.app_label, opts.module_name), obj):
            perms_needed = True
        objects.append([obj,[]])
    return objects, perms_needed

def add_list_to_session(request, key):
    request.session[session_key] = items = get_objects(request, key)
    return items

def delete_list_from_session(request):
    if session_key in request.session:
        items = request.session.get(session_key)
        del request.session[session_key]
        return items
    return []

def check_permission(user, permission, obj):
    app_label = obj._meta.app_label
    model_name = obj._meta.module_name 
    return user.has_perm('%s.%s_%s' %(app_label, permission, model_name), obj)

def check_permissions(user, permission, tuples_list, object=None):
    real_models = []
    for key, value in tuples_list:
        arr = key.split('__')
        app_label = arr[0]
        model_name = arr[1]
        has_perm = user.has_perm('%s.%s_%s' %(app_label, permission, model_name), object)
        if has_perm:
            real_models.append((key, value))
    return real_models

def container_models(container):
    cts = []
    if container.allowed_models:
        ct_ids = container.allowed_models.split(',')
        for ct_id in ct_ids:
            try:
                ct = ContentType.objects.get(pk=ct_id)
            except (MultipleObjectsReturned, ObjectDoesNotExist):
                pass
            else:
                cts.append(ct)
    return cts

def all_container_models(admin_site):
    cts = []
    for model, model_admin in admin_site._registry.items():
        if issubclass(model, Node): 
            model_name = model._meta.module_name
            app_label = model._meta.app_label
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name)
            except (MultipleObjectsReturned, ObjectDoesNotExist):
                pass
            else:
                cts.append(ct)
    return cts   

def container_models(container, admin_site):
#    cts = container_models(container)
#    if cts:
#        return cts
    return all_container_models(admin_site)