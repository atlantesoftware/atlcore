#coding=UTF-8
from django.conf import settings
from django.utils.functional import update_wrapper
from django import template
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin, messages
from django.contrib.admin import AdminSite
from django.contrib.contenttypes.models import ContentType
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied, MultipleObjectsReturned, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models.base import ModelBase
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect
#from docutils.readers.python.pynodes import parameter

from atlcore.site.mediaenvironment import MediaEnvironment
from atlcore import settings as atlsettings
from atlcore.cms.component_manager import ComponentManager
from atlcore.contenttype.admin import delete_selected
from atlcore.contenttype.models import Node, Container

class NotRegistered(Exception):
    pass

from .clipboard import Clipboard

csrf_protect_m = method_decorator(csrf_protect)

use_atl_workflow = False
if 'atlcore.workflows' in settings.INSTALLED_APPS:
    try:
        from atlcore.workflows.models import Workflow, Transition
    except ImportError:
        pass
    else:
        use_atl_workflow = True

admin.autodiscover()

class CountExceed(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Panel(AdminSite):
    
    index_template = '%s/cms/templates/admin/cms/index.html' %atlsettings.DIRECTORY
#    app_index_template = '%s/cms/templates/admin/cms/app_index.html' %atlsettings.DIRECTORY
    login_template = '%s/cms/templates/registration/cms/login.html' %atlsettings.DIRECTORY
    logout_template = '%s/cms/templates/registration/cms/logout.html' %atlsettings.DIRECTORY
    password_change_template = '%s/cms/templates/registration/cms/password_change.html' %atlsettings.DIRECTORY
    password_change_done_template = '%s/cms/templates/registration/cms/password_change_done.html' %atlsettings.DIRECTORY
 
    def __init__(self, name='admin', app_name='admin'):
        super(Panel, self).__init__(name=name, app_name=app_name)
        self.clipboard = Clipboard()
        self._registry = admin.site._registry
        #self.root_path = '/media/'
        
    def unregister_nodes(self, model_or_iterable):
        """
        Unregisters all models derived from Node except the given model(s).

        If a model isn't already registered, this will raise NotRegistered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model, admin_model in self._registry.items():
            if isinstance(model, Node) and model not in model_or_iterable:
                if model not in self._registry:
                    raise NotRegistered('The model %s is not registered' % model.__name__)
                del self._registry[model]
                
    def get_component_manager(self, request, admin_site, instance=None, context={}):
        return ComponentManager(request, admin_site, instance, context)
                
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url, include

        if settings.DEBUG:
            self.check_dependencies()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        
        urlpatterns = self.clipboard.get_urls()

        # Add in each model's views.
        for model, model_admin in self._registry.iteritems():
            urlpatterns += patterns('',
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.module_name), include(model_admin.urls))
            )
            if issubclass(model, Node):
                urlpatterns += patterns('',
                    url(r'^', include(model_admin.get_container_add_url))
                )
        urlpatterns += patterns('',
            url(r'^container/(?P<container_id>[a-fA-F0-9]+)/$', self.container_view, name='container-view')
        )
        urlpatterns += patterns('',
            url(r'^conf/$', self.admin_view(self.conf), name="conf-url"),
            url(r'^atlconf/$', self.admin_view(self.atl_conf), name="atl-conf-url"),
            url(r'^delete_selected/$', self.admin_view(self.delete_selected), name="delete-selected"),
            url(r'^i18n/setlang/$', 'django.views.i18n.set_language', name='setlang'),
        )
        if use_atl_workflow:
            urlpatterns += patterns('', 
                url(r'^modelsworkflow/$', self.admin_view(self.modelsworkflow), name="models-workflow"),
                url(r'^transitionto/(?P<generic_id>[a-fA-F0-9]+)/(?P<transition_id>\d+)/$', self.admin_view(self.workflow_state_transition), name="transition_to"),
            )

        # Admin-site-wide views.
        urlpatterns += patterns('',
            url(r'^$',
                wrap(self.index),
                name='index'),
            url(r'^logout/$',
                wrap(self.logout),
                name='logout'),
            url(r'^password_change/$',
                wrap(self.password_change, cacheable=True),
                name='password_change'),
            url(r'^password_change/done/$',
                wrap(self.password_change_done, cacheable=True),
                name='password_change_done'),
            url(r'^jsi18n/$',
                wrap(self.i18n_javascript, cacheable=True),
                name='jsi18n'),
            url(r'^r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$',
                'django.views.defaults.shortcut'),
            url(r'^(?P<app_label>\w+)/$',
                wrap(self.app_index),
                name='app_list')
        )
        # VCL Data Providers
        
        urlpatterns += patterns('',
            (r'', include(self.get_main_grid_urls())),
        )
        
        from atlcore.vcl.dataproviders.jstree import JSTreeContainerProvider
        urlpatterns += patterns('',
            (r'', include(JSTreeContainerProvider.get_urls())),
        )
              
        return urlpatterns
    
    def get_main_grid_urls(self):
        from atlcore.vcl.dataproviders.jqgrid import JQGridNodeProvider
        return JQGridNodeProvider.get_urls()

    def get_AtlNode_models(self, request=None):
        models = []
        for model, model_admin in self._registry.items():
            app_label = model._meta.app_label
            if issubclass(model, Node): 
                model_name = model._meta.module_name
                name = capfirst(model._meta.object_name)
                model_key = "%s__%s" %(app_label, model_name)
                models.append((model_key, name))
        return models
    
    def __atl_models_dic__(self, request):
        """

        """       
        roots = []
        contents = []
        containers = []
        menu_tree = []
        user = request.user
        for model, model_admin in self._registry.items():
            app_label = model._meta.app_label
            if issubclass(model, Node):
                model_name = model._meta.module_name
                name = capfirst(model._meta.object_name)
                model_key = "%s__%s" %(app_label, model_name)
                if issubclass(model, Container):
                    #m_roots = read_access_filter(user, Container.objects.filter(content_type__model=model_name)) 
                    m_roots = Container.objects.filter(content_type__model=model_name)
                    if m_roots:                            
                        roots.append((m_roots, model_name))
                    containers.append((model_key, name))
                else:
                    contents.append((model_key, name))
        context = {
            'roots_list': roots,
            'contents_model': contents,
            'containers_model': containers,
        }
        return context
    
    def container_view(self, request, container_id=None):
        request.session['container_id'] = container_id
        container = Container.objects.get(id=container_id)
        #component_manager = ComponentManager(request, self, instance=container)
        component_manager = self.get_component_manager(request, self, instance=container)
        context = {
            'title': _('AtlCMS admin home'),
        }
        context.update(component_manager.get_context())     
        context_instance = template.RequestContext(request, current_app=self.name)
        templates = [
            'admin/cms/index.html',
            'admin/index.html'
        ]
        return render_to_response(self.index_template or templates, context, context_instance=context_instance)
       
    def index(self, request, extra_context=None): 
        request.session['container_id'] = None
        #component_manager = ComponentManager(request, self)
        component_manager = self.get_component_manager(request, self)  
        context = {
            'title': _('AtlCMS admin home'),
        }
        context.update(component_manager.get_context())     
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.name)
        templates = [
            'admin/cms/index.html',
            'admin/index.html'
        ]
        return render_to_response(self.index_template or templates, context, context_instance=context_instance)
        
    def app_index(self, request, app_label, extra_context=None):
        ctypes = ContentType.objects.filter(app_label=app_label)
        is_atl_conf = False
        for ct in ctypes:
            model = ct.model_class()
            if issubclass(model, Node):
                is_atl_conf = True
                break            
        context = {
            'is_atl_conf':is_atl_conf,
        }
        context.update(extra_context or {})
        return super(Panel, self).app_index(request, app_label, context)
    
    def conf(self, request, is_atl=False):
        """
        """
        app_dict = {}
        roots = []
        contents = []
        containers = []
        menu_tree = []
        user = request.user
        for model, model_admin in self._registry.items():
            app_label = model._meta.app_label
            has_module_perms = user.has_module_perms(app_label)
            if has_module_perms:
                perms = model_admin.get_model_perms(request)
                if True in perms.values():
                    if (not is_atl and not issubclass(model, Node)) or (is_atl and issubclass(model, Node)):
                        model_dict = {
                            'name': capfirst(model._meta.object_name),
                            'admin_url': mark_safe('%s/%s/' % (app_label, model.__name__.lower())),
                            'perms': perms,
                        }
                        if app_label in app_dict:
                            app_dict[app_label]['models'].append(model_dict)
                        else:
                            app_dict[app_label] = {
                                'name': app_label.title(),
                                'app_url': app_label + '/',
                                'has_module_perms': has_module_perms,
                                'models': [model_dict],
                            }
    
    
        # Sort the apps alphabetically.
        app_list = app_dict.values()
        app_list.sort(lambda x, y: cmp(x['name'], y['name']))
    
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(lambda x, y: cmp(x['name'], y['name']))
        
        #Obteniendo el Jstree
        from atlcore.contenttype.models import Container
        from atlcore.vcl.components import JSTree
        from django.utils.translation import get_language
        containerlist = Container.objects.filter(parent=None).order_by('-order')
         
        media_environment= MediaEnvironment()
        context = {
            'title': _('AtlCMS configuration page'),
            'app_list': app_list,
            'is_atl_conf': is_atl,
            'use_atl_workflow': use_atl_workflow,
            'media_environment' : media_environment,
        }
        #component_manager = ComponentManager(request, self)
        component_manager = self.get_component_manager(request, self)  
        context.update(component_manager.get_context()) 
        context_instance = template.RequestContext(request, current_app=self.name)
        return render_to_response('admin/cms/configuration.html', context, context_instance=context_instance)
    
    
    def atl_conf(self, request):
        return self.conf(request, is_atl=True)    

    def delete_selected(self, request):
        url = reverse('admin:index')
        if request.method == 'POST':
            return delete_selected(request, self, url)
        return HttpResponseRedirect(url)

    def modelsworkflow(self, request, template_name='admin/workflows/models_workflow.html'):
        """
        """
        global_perms = False
        if use_atl_workflow:
            workflows = Workflow.objects.all()        
            models = []
            user = request.user
            for model, model_admin in self._registry.items():
                if issubclass(model, Node):
                    app_label = model._meta.app_label
                    model_name = model._meta.module_name
                    perm = '%s.change_%s' %(app_label, model_name)
                    if user.has_perm(perm):
                        global_perms = True
                        ct = ContentType.objects.get_for_model(model)
                        wf = Workflow.get_workflow_for_model(ct)                 
                        if request.method == 'POST' and request.POST.has_key('%s__%s'%(app_label, model_name)) and request.POST.has_key('workflow__%s__%s'%(app_label, model_name)):
                            wf_id = request.POST.get('workflow__%s__%s'%(app_label, model_name))
                            if wf_id != 'null' and (wf is None or unicode(wf.id) != wf_id):
                                try:
                                    wf = Workflow.objects.get(pk=wf_id)
                                except Workflow.DoesNotExist:
                                    pass
                                else:
                                    Workflow.set_workflow_for_model(ct, wf)                                
                            elif wf_id == 'null' and wf is not None:
                                Workflow.remove_workflow_from_model(ct)
                                wf = None
                        models.append((app_label, model_name, wf))
        else:
            workflows = []
            models = []
        context = {
            'title': _('Models & Workflow relations'),
            'models': models,
            'workflows': workflows,
            'permissions': global_perms,
        }
        context_instance = template.RequestContext(request, current_app=self.name)
        return render_to_response(template_name, context, context_instance=context_instance)
    
    def workflow_state_transition(self, request, generic_id, transition_id):
        url = None
        try:
            generic = Node.objects.get(pk=generic_id)
            transition = Transition.objects.get(pk=transition_id)
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            pass
        else:
            obj = generic.get_instance()
            done = Transition.do_transition(obj, transition, request.user)
            url = obj.admin_url()
            msg = _('Transition to') + ' ' + transition.destination.name + ' '
            if done:                
                messages.info(request, msg + 'was done successfully')
            else:
                messages.info(request, msg + 'cannot be done')
        if url is None:
            url = request.META.get('HTTP_REFERER', None)
        if url is None:
            url = reverse('admin:index')
        return HttpResponseRedirect(url) 
