#coding=UTF-8

from django import template
from django.contrib import admin
from django.contrib.admin.util import unquote
from django.contrib.auth.models import User, Group
from django.conf.urls.defaults import patterns, url
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

csrf_protect_m = method_decorator(csrf_protect)

from atlcore.permissions.models import ADD, READ, CHANGE, DELETE

from atlcore.workflows.models import State
from atlcore.workflows.models import AtlOwnerStatePermission
from atlcore.workflows.models import AtlUserStatePermission
from atlcore.workflows.models import AtlGroupStatePermission
from atlcore.workflows.models import StateObjectRelation
from atlcore.workflows.models import Transition
from atlcore.workflows.models import Workflow
from atlcore.workflows.models import WorkflowObjectRelation
from atlcore.workflows.models import WorkflowModelRelation

class StateInline(admin.TabularInline):
    model = State

class WorkflowAdmin(admin.ModelAdmin):
    inlines = [
        StateInline,
    ]

class StateAdmin(admin.ModelAdmin):
    
    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.module_name
        urls = super(StateAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(?P<state_id>.+)/permissions/$', self.admin_site.admin_view(self.permissions_view), name='%s_%s_permissions' % info),  
        )
        return my_urls + urls
    
    @csrf_protect_m
    def permissions_view(self, request, state_id, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label
        module_name = opts.module_name
        try:
            state = self.queryset(request).get(pk=unquote(state_id))
            
        except self.model.DoesNotExist:
            # Don't raise Http404 just yet, because we haven't checked
            # permissions yet. We don't want an unauthenticated user to be able
            # to determine whether a given object exists.
            state = None

        if state is None:
            raise Http404(_('%(name)s state with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(state_id)})
        
        if not self.has_change_permission(request, state):
            raise PermissionDenied    
                
        t_users_perm = AtlUserStatePermission.objects.filter(state__id = unquote(state_id))
        t_users = User.objects.exclude(is_superuser=True)
        for usr_p in t_users_perm:
            t_users = t_users.exclude(pk=usr_p.user.id)        

        t_groups_perm = AtlGroupStatePermission.objects.filter(state__id = unquote(state_id))
        t_groups = Group.objects.all()
        for grp_p in t_groups_perm:
            t_groups = t_groups.exclude(pk=grp_p.group.id)
        
        
        if request.method == 'POST':
            
            owner_perm_qs = AtlOwnerStatePermission.objects.filter(state__id = unquote(state_id))
            o_add_key = "owner_add"
            o_read_key = "owner_read"
            o_change_key = "owner_change"
            o_delete_key = "owner_delete"
            o_permission = 0
            if request.POST.has_key(o_add_key):
                o_permission += ADD
            if request.POST.has_key(o_read_key):
                o_permission += READ
            if request.POST.has_key(o_change_key):
                o_permission += CHANGE
            if request.POST.has_key(o_delete_key):
                o_permission += DELETE
            if owner_perm_qs and o_permission == 0:
                owner_perm_qs.delete()
            elif owner_perm_qs and o_permission > 0:
                for owner_perm in owner_perm_qs:
                    if not unicode(o_permission) == owner_perm.codename:
                        owner_perm.codename = unicode(o_permission)
                        owner_perm.save()
            elif not owner_perm_qs and o_permission > 0:
                owner_perm = AtlOwnerStatePermission()
                owner_perm.state = state
                owner_perm.codename = unicode(o_permission)
                owner_perm.save()
            
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
                    n_user_perm = AtlUserStatePermission()
                    n_user_perm.state = state
                    n_user_perm.user = user
                    n_user_perm.codename = unicode(t_permission)
                    n_user_perm.save()    
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
                    n_group_perm = AtlGroupStatePermission()
                    n_group_perm.state = state
                    n_group_perm.group = group
                    n_group_perm.codename = unicode(t_permission)
                    n_group_perm.save()
            #refrescando los cambios realizados en el post           
            t_users_perm = AtlUserStatePermission.objects.filter(state__id=unquote(state_id))
            t_users = User.objects.exclude(is_superuser=True)
            for usr_p in t_users_perm:
                t_users = t_users.exclude(pk=usr_p.user.id)        
    
            t_groups_perm = AtlGroupStatePermission.objects.filter(state__id=unquote(state_id))
            t_groups = Group.objects.all()
            for grp_p in t_groups_perm:
                t_groups = t_groups.exclude(pk=grp_p.group.id) 
                
        owner_perm_qs = AtlOwnerStatePermission.objects.filter(state__id = unquote(state_id))
        if owner_perm_qs:
            owner = owner_perm_qs[0]
        else:
            owner = None
                    
        context = {
            "title": _("Permissions"),
            "opts": opts,
            "state": state,
            "app_label": app_label,
            "users":t_users,
            "groups":t_groups,
            "users_perm":t_users_perm,
            "groups_perm":t_groups_perm,
            "action_name":_('permissions'),
            "has_change_permission":True,
            'owner': owner,
        }
        context.update(extra_context or {})
        context.update(csrf(request))
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response([
                    "admin/%s/%s/state_permissions.html" % (app_label, opts.object_name.lower()),
                    "admin/%s/state_permissions.html" % app_label,
                    "admin/state_permissions.html"
                ], context, context_instance=context_instance)


admin.site.register(Workflow, WorkflowAdmin)

admin.site.register(State, StateAdmin)
#admin.site.register(StateInheritanceBlock)
admin.site.register(StateObjectRelation)
#admin.site.register(StatePermissionRelation)
admin.site.register(Transition)
admin.site.register(WorkflowObjectRelation)
admin.site.register(WorkflowModelRelation)
#admin.site.register(WorkflowPermissionRelation)