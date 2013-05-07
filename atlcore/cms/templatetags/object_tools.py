#coding=UTF-8
from atlcore.cms.admin import panel
from atlcore.contenttype import helper
from atlcore.contenttype.models import Container

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _, get_language

register = template.Library()

use_atl_workflow = False
if 'atlcore.workflows' in settings.INSTALLED_APPS:
    try:
        from atlcore.workflows.models import Workflow, Transition, State
    except ImportError:
        pass
    else:
        use_atl_workflow = True

def object_tools(context, current_view):
    user = context.get('user', None)
    can_add = False
    can_change = False
    can_delete = False
    is_index = False
    is_folder = False
    objects_model = None
    delete_selected_url = None
    copy_selected_url = None
    cut_selected_url = None
    paste_selected_url = None
    wf_context = None
    conf_selected_url = None
    languages = list(context.get('LANGUAGES', []))
    lang_code = [get_language()]
    if 'object' in context:
        obj = context['object']
    elif 'original' in context:
        obj = context['original']
    else:
        obj = None
        objects_model = helper.check_permissions(user, 'add', context['containers_model'])
        if objects_model: can_add = True
        is_index = True
        delete_selected_url = reverse('admin:delete-selected')
#        copy_selected_url = reverse('admin:copy-list-to-clipboard')
#        cut_selected_url = reverse('admin:move-list-to-clipboard')
#        paste_selected_url = reverse('admin:paste-from-clipboard', args=[0])
    if obj:
        can_change = helper.check_permission(user, 'change', obj)
        ctype = ContentType.objects.get_for_model(obj)
        if use_atl_workflow:            
            wf = Workflow.get_workflow_for_model(ctype)
            if wf is not None:
                transitions = Transition.get_allowed_transitions(obj, user)
                wf_context = {
                    'wf_current_state': State.get_state(obj), 
                    'wf_states': [(t.id, t.name) for t in transitions],         
                }
        if isinstance(obj, Container):
            opts = obj._meta
            admin_model = panel._registry.get(ctype.model_class(), None)
            if admin_model is not None:
                cts = helper.container_models(obj, admin_model.admin_site)
                container_models = []
                for ct in cts:        
                    obj_model = ct.model_class()
                    pt = '%s.%s' %(opts.app_label, opts.module_name)
                    if pt in obj_model.PARENT_TYPES:     
                        model_key = "%s__%s" %(ct.app_label, ct.model)
                        name = capfirst(ct.model)
                        container_models.append((model_key, name))
                objects_model = helper.check_permissions(user, 'add', container_models, obj)
            else:
                objects_model = helper.check_permissions(user, 'add', context['containers_model'] + context['contents_model'], obj)
            if objects_model: can_add = True
            is_folder = True            
            delete_selected_url = obj.admin_delete_selected()
#            copy_selected_url = reverse('admin:copy-list-to-clipboard')
#            cut_selected_url = reverse('admin:move-list-to-clipboard')
#            paste_selected_url = reverse('admin:paste-from-clipboard', args=[obj.id])
#            conf_selected_url = reverse('admin:%s_%s_conf'%(opts.app_label, opts.module_name), args=[obj.id])
        else:
            can_delete = helper.check_permission(user, 'delete', obj)
#            copy_selected_url = reverse('admin:copy-object-to-clipboard', args=[obj.get_generic().id])
#            cut_selected_url = reverse('admin:move-object-to-clipboard', args=[obj.get_generic().id])
            #lang_code = [obj.language]
            #trans = obj.get_translations()
            #lang_code += [t.language for t in trans]
    #eliminando el lenguaje del contenido de la lista de traducciones a realizar
    final_langs = [(c,n) for c,n in languages if not c in lang_code]      
    tag_context = {
        'objects_model': objects_model,
        'object': obj,
        'LANGUAGES': final_langs,
        #devuelven verdadero o falso para saber cuando un link se pone activo o no.
        #grupo1
        'addlink': can_add and 'add' != current_view,
        'changelink': can_change and 'change' != current_view,
        'deletelink': can_delete and not is_folder,
        'delete_selected_url': delete_selected_url,
        #grupo2
        'copylink': obj is not None and not is_folder,
        'copy_selected_url': copy_selected_url,
        'cutlink': obj is not None and not is_folder,
        'cut_selected_url': cut_selected_url,
        #'pastelink': (obj is None or is_folder) and context['can_paste_from_clipboard'],
        'paste_selected_url': paste_selected_url,
        #grupo3
        'detaillink': 'details' != current_view,
        'summarylink': (is_folder or is_index) and 'summary' != current_view,
        'thumbnaillink': (is_folder or is_index) and 'thumbnails' != current_view,
        'viewsitelink': obj is not None,
        #grupo4
        #'translate': obj is not None, # and not is_folder,
        #grupo5
        'historylink': obj is not None and 'history' != current_view,
        #grupo6
        'permissionslink': can_change and 'permissions' != current_view,
        #group7
        'use_atl_workflow': wf_context is not None,
        #group7
        #'has_url_conf': conf_selected_url is not None and 'configuration' != current_view,
        #'conf_selected_url': conf_selected_url,
    }
    tag_context.update(wf_context or {})
    context.update(tag_context)
    return context
object_tools = register.inclusion_tag('admin/cms/includes/object_tools.html', takes_context=True)(object_tools)
