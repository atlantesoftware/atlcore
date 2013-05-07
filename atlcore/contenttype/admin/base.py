#coding=UTF-8
from datetime import datetime

#
from django import template
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.forms.formsets import all_valid
from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, widgets, helpers
from django.contrib.admin.util import unquote, get_deleted_objects
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied, MultipleObjectsReturned, ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.db import models, transaction, router
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.functional import update_wrapper
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _, ungettext
from django.utils.encoding import force_unicode, iri_to_uri
from django.template.defaultfilters import escapejs
from django.forms.widgets import HiddenInput, TextInput

from atlcore import settings as atlsettings
from atlcore.aspect.fields import AtlAspectField
from atlcore.cms.component_manager import ComponentManager
from atlcore.contenttype.models import Node, Container
from atlcore.contenttype.context_processors import templates as templates_cp
#from atlcore.atl_aspect.fields import AtlAspectField
from atlcore.contenttype.admin.delete_selected import delete_selected
#from atlcore.atl_content_type.admin.helpers import read_access_filter, change_access_filter, get_deleted_objects
#from atlcore.atl_content_type.models import Folder, AtlNode, Container, update_m2m_generic
from atlcore.permissions.forms import AtlPermissionForm, AtlUserPermissionForm, AtlGroupPermissionForm
from atlcore.permissions.models import AtlUserPermission, AtlGroupPermission, ADD, CHANGE, DELETE, READ


csrf_protect_m = method_decorator(csrf_protect)
#
#use_atl_workflow = False
#if 'atlcore.atl_workflows' in settings.INSTALLED_APPS:
#    try:
#        from atlcore.atl_workflows.models import Workflow
#    except ImportError:
#        pass
#    else:
#        use_atl_workflow = True
#
#def __set_session_folder__(obj, request):
#    if isinstance(obj, Folder):
#        folder_id = obj.id
#        folder = obj
#    else:
#        folder_id = obj.folder_id        
#        try:
#            folder = Folder.objects.get(pk=folder_id)
#        except (MultipleObjectsReturned, ObjectDoesNotExist):
#            folder = None
#    request.session['folder_id'] = folder_id
#    return folder_id, folder
#
#def set_session_folder(folder_id, request):
#    request.session['folder_id'] = folder_id
#

class Base(admin.ModelAdmin):
    
    change_form_template = '%s/cms/templates/admin/cms/change_form.html' %atlsettings.DIRECTORY
    add_form_template = '%s/cms/templates/admin/cms/add_form.html' %atlsettings.DIRECTORY
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'view_count')
    ordering = ['-view_count']
    search_fields = ['title', "description" ]
    
    def save_form(self, request, form, change):
        form.request = request
        return super(Base, self).save_form(request, form, change)    

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Hook for specifying the form Field instance for a given database Field
        instance.

        If kwargs are given, they're passed to the form Field's constructor.
        """
        request = kwargs.pop("request", None)


        if db_field.name == 'owner':
            return db_field.formfield(widget= TextInput)

        # If the field specifies choices, we don't need to look for special
        # admin widgets - we just need to use a select widget of some kind.
        if db_field.choices:
            return self.formfield_for_choice_field(db_field, request, **kwargs)

        # ForeignKey or ManyToManyFields
        if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
            # Combine the field kwargs with any options for formfield_overrides.
            # Make sure the passed in **kwargs override anything in
            # formfield_overrides because **kwargs is more specific, and should
            # always win.
            if db_field.__class__ in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[db_field.__class__], **kwargs)

            # Get the correct formfield.
            if isinstance(db_field, models.ForeignKey):
                formfield = self.formfield_for_foreignkey(db_field, request, **kwargs)
            elif isinstance(db_field, models.ManyToManyField):
                formfield = self.formfield_for_manytomany(db_field, request, **kwargs)

            # For non-raw_id fields, wrap the widget with a wrapper that adds
            # extra HTML -- the "add other" interface -- to the end of the
            # rendered output. formfield can be None if it came from a
            # OneToOneField with parent_link=True or a M2M intermediary.
            if formfield and db_field.name not in self.raw_id_fields and not isinstance(db_field, AtlAspectField):
                formfield.widget = widgets.RelatedFieldWidgetWrapper(formfield.widget, db_field.rel, self.admin_site)

            return formfield

        # If we've got overrides for the formfield defined, use 'em. **kwargs
        # passed to formfield_for_dbfield override the defaults.
        for klass in db_field.__class__.mro():
            if klass in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[klass], **kwargs)
                return db_field.formfield(**kwargs)

        # For any other type of field, just call its formfield() method.
        return db_field.formfield(**kwargs)
    
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.changelist_view),
                name='%s_%s_changelist' % info),
            url(r'^(?P<object_id>.+)/delete_selected/$', self.admin_site.admin_view(self.delete_selected_view), name='%s_%s_delete_selected' % info),
            url(r'^(?P<object_id>.+)/details/$', self.admin_site.admin_view(self.details_view), name='%s_%s_details' % info),
            url(r'^(?P<object_id>.+)/permissions/$', self.admin_site.admin_view(self.permissions_view), name='%s_%s_permissions' % info),
            url(r'^(?P<object_id>.+)/settings/$', self.admin_site.admin_view(self.container_settings), name='%s_%s_settings' % info),               
            url(r'^None/$', self.admin_site.index, name='%s_%s_none_details' % info),
            url(r'^add/$',
                wrap(self.add_view),
                name='%s_%s_add' % info),
            url(r'^(.+)/history/$',
                wrap(self.history_view),
                name='%s_%s_history' % info),
            url(r'^(.+)/delete/$',
                self.delete_view,
                name='%s_%s_delete' % info),
            url(r'^(.+)/$',
                wrap(self.change_view),
                name='%s_%s_change' % info),
        )
        return urlpatterns
    
#    def get_urls(self):
#        info = self.model._meta.app_label, self.model._meta.module_name
#        urls = super(Base, self).get_urls() 
#        my_urls = patterns('',
#            url(r'^(?P<object_id>.+)/delete_selected/$', self.admin_site.admin_view(self.delete_selected_view), name='%s_%s_delete_selected' % info),
#            url(r'^(?P<object_id>\d+)/details/$', self.admin_site.admin_view(self.details_view), name='%s_%s_details' % info),
#            url(r'^None/$', self.admin_site.index, name='%s_%s_none_details' % info),
#        )
#        return my_urls + urls   
    
    def get_component_manager(self, request, admin_site, instance=None, context={}):
        return ComponentManager(request, admin_site, instance, context)
        
    @csrf_protect_m
    @transaction.commit_on_success
    def delete_view(self, request, object_id, extra_context=None):
        "The 'delete' admin view for this model."
        extra_context = self.__base_view__(request, object_id, extra_context)
        opts = self.model._meta
        app_label = opts.app_label

        obj = self.get_object(request, unquote(object_id))

        if not self.has_delete_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        using = router.db_for_write(self.model)

        # Populate deleted_objects, a data structure of all related objects that
        # will also be deleted.
        (deleted_objects, perms_needed, protected) = get_deleted_objects([obj], opts, request.user, self.admin_site, using)

        if request.POST: # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_unicode(obj)
            self.log_deletion(request, obj, obj_display)
            obj.delete()

            self.message_user(request, _('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})

            if obj.parent is not None:
                obj_parent = obj.parent
                url_to_redirect = '/%s/%s/%s/%s/details' % (atlsettings.ADMIN_PREFIX, obj_parent.content_type.app_label, obj_parent.content_type.model, obj_parent.id)
            else:
                url_to_redirect = '/%s' % atlsettings.ADMIN_PREFIX
            
            return HttpResponseRedirect(url_to_redirect)
        

        context = {
            "title": _("Are you sure?"),
            "object_name": force_unicode(opts.verbose_name),
            "object": obj,
            "deleted_objects": deleted_objects,
            "perms_lacking": perms_needed,
            "opts": opts,
            #"root_path": self.admin_site.root_path,
            "app_label": app_label,
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.delete_confirmation_template or [
            "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_confirmation.html" % app_label,
            "admin/delete_confirmation.html"
        ], context, context_instance=context_instance)
    
    
    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Determines the HttpResponse for the add_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if request.POST.has_key("_popup"):
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if request.POST.has_key("_popup"):
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(pk_value), escapejs(obj)))
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)
            # Redirecciono para la vista del contenedor del padre del objeto creado
            if obj.parent is not None:
                obj_parent = obj.parent
                url_to_redirect = '/%s/%s/%s/%s/details' % (atlsettings.ADMIN_PREFIX, obj_parent.content_type.app_label, obj_parent.content_type.model, obj_parent.id)
            else:
                url_to_redirect = '/%s' % atlsettings.ADMIN_PREFIX
            
            return HttpResponseRedirect(url_to_redirect)


    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if request.REQUEST.has_key('_popup'):
                return HttpResponseRedirect(request.path + "?_popup=1")
            else:
                return HttpResponseRedirect(request.path)
        elif request.POST.has_key("_saveasnew"):
            msg = _('The %(name)s "%(obj)s" was added successfully. You may edit it again below.') % {'name': force_unicode(opts.verbose_name), 'obj': obj}
            self.message_user(request, msg)
            return HttpResponseRedirect("../%s/" % pk_value)
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect("../add/")
        else:
            self.message_user(request, msg)
            if obj.parent is not None:
                obj_parent = obj.parent
                url_to_redirect = '/%s/%s/%s/%s/details' % (atlsettings.ADMIN_PREFIX, obj_parent.content_type.app_label, obj_parent.content_type.model, obj_parent.id)
            else:
                url_to_redirect = '/%s' % atlsettings.ADMIN_PREFIX
            return HttpResponseRedirect(url_to_redirect)
    
    def get_container_add_url(self):
        urlpatterns = patterns('', 
            url(r'^%s/container/None/%s_add/$' % (self.model._meta.app_label, self.model._meta.module_name), self.admin_site.admin_view(self.add_to_container_view), name='index_add_%s' % self.model._meta.module_name),
            url(r'^%s/container/(?P<container_id>.+)/%s_add/$' % (self.model._meta.app_label, self.model._meta.module_name), self.admin_site.admin_view(self.add_to_container_view), name='container_add_%s' % self.model._meta.module_name),            
        ) 
        return urlpatterns 
    get_container_add_url = property(get_container_add_url)
    
    def __relations_context__(self, obj):            
        try:
            from atlcore.relations.models import AtlRelation, AtlRelationsInstance
        except ImportError:
            rel_dict = {}
        else:
            relations = AtlRelationsInstance.objects.for_this_object_with_pos(obj)
            relation_types = AtlRelation.objects.for_this_class_with_pos(obj.__class__)
            rel_dict = {
                'relations':relations,
                'relation_types':relation_types,
                'relation_object':obj,
                'content_type_id':ContentType.objects.get_for_model(obj).id,
            }            
        return rel_dict
    
    def __base_view__(self, request, object_id, extra_context):
        opts = self.model._meta
        app_label = opts.app_label
        obj = self.get_object(request, unquote(object_id))

#        if not self.has_read_permission(request, obj):
#            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
        
        change_perm = self.has_change_permission(request, obj)
        
        is_container = issubclass(self.model, Container)
        
        if is_container:             
            original_contents = obj.children.all()
            #original_len = len(original_contents)
            contents = original_contents #contents = read_access_filter(request.user, original_contents)
            #filtered_len = len(contents)
            #if change_perm: change_perm = original_len == filtered_len == len(change_access_filter(request.user, original_contents))
            
            paginator = Paginator(contents, atlsettings.ADMIN_ELEMENT_BY_PAGE)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                contents_list = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contents_list = paginator.page(paginator.num_pages)
            container_context = {
                'title': obj.title,
                'object_list': contents_list.object_list,
                #'model_list': self.admin_site.get_AtlNode_models(request),
                'pager': contents_list,
                'container_id': obj.id,
                'container': obj,                
            }
        else:
            if obj.parent:
                container = obj.get_parent()
                container_id = container.id
            else:
                container = None
                container_id = 0
            container_context = {
                'title': obj.title,
                #'tool_bar' : self.__create_tool_bar(),
                'container_id': container_id,
                'container': container,                 
            }#{'title': u"%s  (%s: %s)" %(obj.title, _('Visits'), obj.visit_count)}
#            try:
#                from django.contrib.comments import Comment
#                try:
#                    container_context['comments'] = Comment.objects.for_model(obj)
#                except (MultipleObjectsReturned, ObjectDoesNotExist):
#                    pass                
#            except ImportError:
#                pass
            
        context = {
            'module_name': force_unicode(opts.verbose_name_plural),
            #'has_add_permission': self.has_add_permission(request, obj),
            #'root_path': self.admin_site.root_path,
            'app_label': app_label,
            'opts': opts,
            'object': obj,
            'is_container': is_container,
            'change_perm':change_perm,
#            'use_atl_workflow': use_atl_workflow,
        }
        node = Node.objects.get(id=object_id)
        #component_manager = ComponentManager(request, self.admin_site, instance=obj)
        component_manager = self.get_component_manager(request, self.admin_site, instance=obj)       
        request.COOKIES['container_id'] = obj
        context.update(component_manager.get_context()) 
#        context.update(self.__relations_context__(obj))
        context.update(container_context or {})
        context.update(extra_context or {})
        return context

#    def change_view(self, request, object_id, extra_context=None):
#        extra_context = self.__base_view__(request, object_id, extra_context)
#        return super(Base, self).change_view(request, object_id, extra_context)

#    def add_view(self, request, form_url='', extra_context=None):        
#        return super(Base, self).add_view(request, form_url, extra_context)
    
    def history_view(self, request, object_id, extra_context=None):
        extra_context = self.__base_view__(request, object_id, extra_context)
        return super(Base, self).history_view(request, object_id, extra_context)
       
    @csrf_protect_m
    def details_view(self, request, object_id, extra_context=None):
        """The 'list' admin view for this model."""
        result = self.__base_view__(request, object_id, extra_context)
        if type(result) == type({}):
            opts = result['opts']
            context_instance = template.RequestContext(request, processors=[templates_cp], current_app=self.admin_site.name)
            return render_to_response([
                '%s/%s/details.html' % (opts.app_label, opts.object_name.lower()),
                '%s/details.html' % opts.app_label,
                'contenttype/node/details.html',
            ], result, context_instance=context_instance)
        return result
    
    def __in_container__(self, request):
        container_id = str(request.session.get('container_id', None))
        try:
            container = Container.objects.get(id=container_id)
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            container = None
        context = {
            'container_id': container_id,
            'container':container,
        }
        return (container is not None, context)

        
    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        if 'container_id' in request.session.keys():
            container_id = request.session['container_id']
            container = Container.objects.get(id=container_id).get_instance()
        else:
            container = None
#        if container_id:
#            container = Container.objects.get(id=container_id).get_instance()
#        else:
#            container = None
        #component_manager = ComponentManager(request, self.admin_site, instance=container)
        component_manager = self.get_component_manager(request, self.admin_site, instance=container)
        context = component_manager.get_context()
        return super(Base, self).add_view(request, form_url=form_url, extra_context=context)


    @csrf_protect_m
    @transaction.commit_on_success
    def add_to_container_view(self, request, container_id=None, form_url='', extra_context=None):
        if container_id:
            container = Container.objects.get(id=container_id).get_instance()
        else:
            container = None
        #component_manager = ComponentManager(request, self.admin_site, instance=container)
        component_manager = self.get_component_manager(request, self.admin_site, instance=container)
        context = component_manager.get_context()
        return super(Base, self).add_view(request, form_url=form_url, extra_context=context)

    
    @csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, extra_context=None):
        #component_manager = ComponentManager(request, self.admin_site)
        component_manager = self.get_component_manager(request, self.admin_site)
        context = component_manager.get_context()
        obj = self.get_object(request, unquote(object_id))
        if obj is not None:        
            context.update(self.__relations_context__(obj))
        return super(Base, self).change_view(request, object_id, extra_context=context)

        
    @csrf_protect_m
    def delete_selected_view(self, request, object_id, extra_context=None):
        """
        """
        if issubclass(self.model, Container):
            try:
                obj = Node.objects.get(pk=object_id)
            except:
                url = reverse('admin:index')
            else:
                url = obj.admin_url()                
            if request.method == 'POST':
                return delete_selected(request, self.admin_site, url)
            return HttpResponseRedirect(url)        
        else: 
            return self.delete_view(request, object_id, extra_context)
        
    def __propagate_user_permissions__(self, request, obj, user, perm_code):
        perm_code = unicode(perm_code)
        descendants = obj.get_descendants()
        user_id = unicode(user.id)
        for desc in descendants:
            if self.has_change_permission(request, desc):
                desc_ct_id = unicode(desc.content_type.id)
                id = unicode(desc.id)
                perms = AtlUserPermission.objects.filter(object_id=id, content_type=desc_ct_id, user__id=user_id)
                tuples = []
                for perm in perms:
                    tuples.append((perm.content_object, perm.user))
                    if unicode(perm.codename) != perm_code:                        
                        if perm_code == '0': 
                            perm.delete()
                        else:
                            perm.codename = perm_code
                            perm.save()
                if not (desc, user) in tuples and perm_code != '0':
                    #Se agrega a la lista de permisos
                    n_user_perm = AtlUserPermission()
                    n_user_perm.content_object = desc
                    n_user_perm.user = user
                    n_user_perm.codename = perm_code
                    n_user_perm.save()                            
            else:
                o = perm.content_object
                self.message_user(request, 'User permissions for "%s: %s" was not changed' %(o._meta.module_name, o.title))
                
    def __propagate_group_permissions__(self, request, obj, group, perm_code):
        perm_code = unicode(perm_code)
        descendants = obj.get_descendants()
        group_id = unicode(group.id)
        for desc in descendants:
            if self.has_change_permission(request, desc):
                desc_ct_id = unicode(desc.content_type.id)
                id = unicode(desc.id)
                perms = AtlGroupPermission.objects.filter(object_id=id, content_type=desc_ct_id, group__id=group_id)
                tuples = []
                for perm in perms:
                    tuples.append((perm.content_object, perm.group))
                    if unicode(perm.codename) != perm_code:                    
                        if perm_code == '0':
                            #Se borra de la lista de permisos si no se le ha asignado permisos.
                            perm.delete()
                        else:
                            #Se actualiza con los nuevos permisos.
                            perm.codename = perm_code
                            perm.save()
                if not (desc, group) in tuples and perm_code != '0':
                    #Se agrega a la lista de permisos
                    n_group_perm = AtlGroupPermission()
                    n_group_perm.content_object = desc
                    n_group_perm.group = group
                    n_group_perm.codename = perm_code
                    n_group_perm.save()
            else:
                o = perm.content_object
                self.message_user(request, 'Permissions for "%s: %s" in group "%s" was not changed' %(o._meta.module_name, o.title, group.title))         
        
        
    @csrf_protect_m
    def permissions_view(self, request, object_id, extra_context=None):
        try:
            node = self.queryset(request).get(pk=unquote(object_id))                
        except self.model.DoesNotExist:
            node = None
        opts = self.model._meta
        app_label = opts.app_label            
        if node is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
        obj = node.get_instance()
        is_container = isinstance(obj, Container)
        if is_container or obj.parent:
            if not self.has_change_permission(request, obj):
                raise PermissionDenied
            ct = obj.content_type            
            t_users_perm = AtlUserPermission.objects.filter(object_id=unquote(object_id), content_type=ct.id)
            t_users = User.objects.exclude(is_superuser=True)
            for usr_p in t_users_perm:
                t_users = t_users.exclude(pk=usr_p.user.id)
            t_groups_perm = AtlGroupPermission.objects.filter(object_id=unquote(object_id), content_type=ct.id)
            t_groups = Group.objects.all()
            for grp_p in t_groups_perm:
                t_groups = t_groups.exclude(pk=grp_p.group.id)
            if request.method == 'POST':
                propagate = request.POST.has_key('propagate')
                for u_perm in t_users_perm:
                    add_key = "user_add_%s" % u_perm.user.id
                    read_key = "user_read_%s" % u_perm.user.id
                    change_key = "user_change_%s" % u_perm.user.id
                    delete_key = "user_delete_%s" % u_perm.user.id
                    t_permission = 0
                    if not request.POST.has_key(add_key) and \
                       not request.POST.has_key(read_key) and \
                       not request.POST.has_key(change_key) and \
                       not request.POST.has_key(delete_key):
                        #delete unchecked users permissions
                        u_perm.delete()
                    else:
                        if request.POST.has_key(add_key):
                            t_permission += ADD
                        if request.POST.has_key(read_key):
                            t_permission += READ
                        if request.POST.has_key(change_key):
                            t_permission += CHANGE
                        if request.POST.has_key(delete_key):
                            t_permission += DELETE
                        #updating users permissions
                        if not unicode(t_permission) == u_perm.codename:
                            u_perm.codename = unicode(t_permission)
                            u_perm.save()
                    if propagate and is_container:
                        self.__propagate_user_permissions__(request, obj, u_perm.user, t_permission)
                for user in t_users:
                    add_key = "user_add_%s" % user.id
                    read_key = "user_read_%s" % user.id
                    change_key = "user_change_%s" % user.id
                    delete_key = "user_delete_%s" % user.id
                    t_permission = 0
                    if request.POST.has_key(add_key):
                        t_permission += ADD
                    if request.POST.has_key(read_key):
                        t_permission += READ
                    if request.POST.has_key(change_key):
                        t_permission += CHANGE
                    if request.POST.has_key(delete_key):
                        t_permission += DELETE
                    if t_permission:
                        #creating a new permissions for this object and user 
                        n_user_perm = AtlUserPermission()
                        n_user_perm.content_object = obj
                        n_user_perm.user = user
                        n_user_perm.codename = unicode(t_permission)
                        n_user_perm.save()
                    if propagate and is_container:
                        self.__propagate_user_permissions__(request, obj, user, t_permission)     
                for u_perm in t_groups_perm:
                    t_permission = 0
                    add_key = "group_add_%s" % u_perm.group.id
                    read_key = "group_read_%s" % u_perm.group.id
                    change_key = "group_change_%s" % u_perm.group.id
                    delete_key = "group_delete_%s" % u_perm.group.id
                    if not request.POST.has_key(add_key) and \
                       not request.POST.has_key(change_key) and \
                       not request.POST.has_key(read_key) and \
                       not request.POST.has_key(delete_key):
                        #delete unchecked groups permissions
                        u_perm.delete()
                    else:
                        if request.POST.has_key(add_key):
                            t_permission += ADD
                        if request.POST.has_key(read_key):
                            t_permission += READ
                        if request.POST.has_key(change_key):
                            t_permission += CHANGE
                        if request.POST.has_key(delete_key):
                            t_permission += DELETE
                        #updating groups permissions
                        if not unicode(t_permission) == u_perm.codename:
                            u_perm.codename = unicode(t_permission)
                            u_perm.save()
                    if propagate and is_container:
                        self.__propagate_group_permissions__(request, obj, u_perm.group, t_permission)   
                for group in t_groups:
                    add_key = "group_add_%s" % group.id
                    read_key = "group_read_%s" % group.id
                    change_key = "group_change_%s" % group.id
                    delete_key = "group_delete_%s" % group.id
                    t_permission = 0
                    if request.POST.has_key(add_key):
                        t_permission += ADD
                    if request.POST.has_key(read_key):
                        t_permission += READ                    
                    if request.POST.has_key(change_key):
                        t_permission += CHANGE
                    if request.POST.has_key(delete_key):
                        t_permission += DELETE
                    if t_permission:
                        #creating a new permissions for this object and group 
                        n_group_perm = AtlGroupPermission()
                        n_group_perm.content_object = obj
                        n_group_perm.group = group
                        n_group_perm.codename = unicode(t_permission)
                        n_group_perm.save()
                    if propagate and is_container:
                        self.__propagate_group_permissions__(request, obj, group, t_permission)
                #refrescando los cambios realizados en el post
                t_users_perm = AtlUserPermission.objects.filter(object_id=unquote(object_id), content_type=ct.id)
                t_users = User.objects.exclude(is_superuser=True)
                for usr_p in t_users_perm:
                    t_users = t_users.exclude(pk=usr_p.user.id)        
        
                t_groups_perm = AtlGroupPermission.objects.filter(object_id=unquote(object_id), content_type=ct.id)
                t_groups = Group.objects.all()
                for grp_p in t_groups_perm:
                    t_groups = t_groups.exclude(pk=grp_p.group.id) 
                        
            context = {
                "title": _("Permissions"),
                "opts": opts,
                "object": obj,
                "app_label": app_label,
                "users":t_users,
                "groups":t_groups,
                "users_perm":t_users_perm,
                "groups_perm":t_groups_perm,
                "action_name":_('Permissions'),
                "is_container": is_container,
            }
            context.update(extra_context or {})
            context.update(csrf(request))
            context_instance = template.RequestContext(request, current_app=self.admin_site.name)
            return render_to_response([
                        "admin/cms/%s/%s/permissions.html" % (app_label, opts.object_name.lower()),
                        "admin/cms/%s/permissions.html" % app_label,
                        "admin/cms/permissions.html"
                    ], context, context_instance=context_instance)
        else:
            url = reverse('admin:index')
            return HttpResponseRedirect(url)            
        
    @csrf_protect_m
    def container_settings(self, request, object_id, extra_context=None):
        """
        Selecciona los modelos que se usan en esa carpeta
        """
        obj = self.get_object(request, unquote(object_id))
        
        opts = self.model._meta

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
        
        if not self.has_change_permission(request, obj):
            raise PermissionDenied
        
        if not issubclass(self.model, Container):
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        all = obj.__class__._registry 
        if request.method == 'POST':
            post_all = request.POST.has_key('all')
            if post_all:
                obj.iregister_all()
            else:
                models = []
                for key, value in all.items():
                    ct = request.POST.get('ct_%s'%key, None)
                    if ct is not None:
                        models.append(value)
                if not models:
                    messages.add_message(request, messages.ERROR, _('At least one option must be marked'))
                else:
                    obj.iunregister_all()
                    obj.iregister(models)
                    messages.add_message(request, messages.INFO, _('The filter for this folder has been changed successfully'))
                    return HttpResponseRedirect(obj.admin_url())
        action_name = _('%s configuration') %obj      
        obj.load_registry()   
        allowed = obj._registry  
        context = {
            'object': obj,
            'action_name': action_name,
            'title': action_name,
            'all': all,
            'allowed': allowed,
            'use_all': all==allowed,
        }
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response([
                    "admin/cms/%s/%s/settings.html" % (opts.app_label, opts.object_name.lower()),
                    "admin/cms/%s/settings.html" % opts.app_label,
                    "admin/cms/settings.html"
                ], context, context_instance=context_instance)
