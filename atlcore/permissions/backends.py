#coding=UTF-8
from atlcore.cms.admin import panel
from atlcore.contenttype.models import Node, Container
from atlcore.permissions.models import AtlUserPermission, AtlGroupPermission

from django.conf import settings
from django.contrib.auth.models import  User, Group, Permission
from django.contrib.auth.backends import ModelBackend
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist

use_atl_workflow = False
if 'atlante_cms.atl_workflows' in settings.INSTALLED_APPS:
    try:
        from atlante_cms.atl_workflows.models import Workflow, State, AtlOwnerStatePermission, AtlUserStatePermission, AtlGroupStatePermission
    except ImportError:
        pass
    else:
        use_atl_workflow = True

def __atl_models_permissions__(permission):
    real_models = []
    for key, value in panel.get_AtlNode_models():
        arr = key.split('__')
        app_label = arr[0]
        model_name = arr[1]
        has_perm = '%s.%s_%s' %(app_label, permission, model_name)
        real_models.append(has_perm)
    return real_models


class AtlUserBackend(object):
    
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
    def get_group_permissions(self, user_obj, obj = None):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        obj_perm = None
        ct = None
        if obj is not None and isinstance(obj, Node):
            try:     
                ct = ContentType.objects.get_for_model(obj) 
                groups_id = Group.objects.filter(user=user_obj).values_list('id', flat=True)
                obj_perm = set()
                for grp_id in groups_id:
                    group_permissions = AtlGroupPermission.objects.filter(object_id=obj.id, content_type=ct.id, group__id = grp_id)                
                    for p in group_permissions:
                        obj_perm |= p.permissions()
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                pass
        workflow_perm = None
        if use_atl_workflow and ct is not None:
            wf = Workflow.get_workflow_for_model(ct)
            if wf is not None:
                state = State.get_state(obj)
                groups = user_obj.groups.all()
                workflow_perm = set()
                for group in groups:
                    permissions = AtlGroupStatePermission.objects.filter(state=state, group=group)
                    for permission in permissions:
                        workflow_perm |= permission.permissions()              
        if obj_perm is not None and workflow_perm is not None:
            obj_perm &= workflow_perm
        if obj_perm is not None:
            if isinstance(obj, Container):
                l = []
                for p in obj_perm:
                    p = p[p.index('.')+1:]
                    p = p[:p.index('_')]
                    l += __atl_models_permissions__(p)
                obj_perm |= set(l)            
            return obj_perm
        if workflow_perm is not None:
            return workflow_perm
        if not hasattr(user_obj, '_group_perm_cache'):
            perms = Permission.objects.filter(group__user=user_obj).values_list('content_type__app_label', 'codename').order_by()
            user_obj._group_perm_cache = set(["%s.%s" % (ct, name) for ct, name in perms])
        return user_obj._group_perm_cache

    def get_all_permissions(self, user_obj, obj = None):
        if user_obj.is_anonymous():
            return set()
        obj_perm = None
        ct = None
        grp_perm = self.get_group_permissions(user_obj, obj)
        if obj is not None and isinstance(obj, Node):
            obj_perm = set()  
            try:
                ct = ContentType.objects.get_for_model(obj) 
                user_permission = AtlUserPermission.objects.get(object_id=obj.id, content_type=ct.id, user=user_obj)
                obj_perm |= user_permission.permissions()
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                pass
        workflow_perm = None
        if use_atl_workflow and ct is not None:
            wf = Workflow.get_workflow_for_model(ct)
            if wf is not None:            
                state = State.get_state(obj)
                workflow_perm = set()
                permissions = AtlUserStatePermission.objects.filter(state=state, user=user_obj)            
                for permission in permissions:
                    workflow_perm |= permission.permissions()                        
        if obj_perm is not None and workflow_perm is not None:
            obj_perm &= workflow_perm  
        if obj_perm is not None:
            if use_atl_workflow and user_obj.id == obj.owner_id:
                state = State.get_state(obj)
                owner_permissions = AtlOwnerStatePermission.objects.filter(state=state)
                for permission in owner_permissions:
                    obj_perm |= permission.permissions()           
            if isinstance(obj, Container):
                l = []
                for p in obj_perm:
                    p = p[p.index('.')+1:]
                    p = p[:p.index('_')]
                    l += __atl_models_permissions__(p)
                obj_perm |= set(l)                       
            return obj_perm | grp_perm
        if workflow_perm is not None:
            return workflow_perm | grp_perm       
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in user_obj.user_permissions.select_related()])
            user_obj._perm_cache.update(self.get_group_permissions(user_obj))
        return user_obj._perm_cache

    def has_perm(self, user_obj, perm, obj = None):
        return perm in self.get_all_permissions(user_obj, obj)
    
    def has_module_perms(self, user_obj, app_label, obj = None):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        for perm in self.get_all_permissions(user_obj, obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False
