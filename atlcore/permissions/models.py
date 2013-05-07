#coding=UTF-8
from atlcore.contenttype.models import Node, Container
#from atlante_cms.atl_countries.models import Country

from django.contrib.auth.models import User, Group
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import ugettext, ugettext_lazy as _

READ = 8
ADD = 4
CHANGE = 2
DELETE = 1
ALL = READ + ADD + CHANGE + DELETE


def __get_permmision_value__(octal_str, pType):    
    try:
        perm = int(octal_str)
    except:
        perm = 0
    if pType == READ:
        return perm >= READ
    if pType == ADD:
        return  perm == ADD or \
                perm == ADD + DELETE or \
                perm == ADD + CHANGE or \
                perm == ADD + READ or \
                perm == ADD + CHANGE + DELETE or \
                perm == ADD + CHANGE + READ or \
                perm == ADD + READ + DELETE or \
                perm == ADD + CHANGE + READ + DELETE
    if pType == CHANGE:
        return  perm == CHANGE or \
                perm == CHANGE + DELETE or \
                perm == CHANGE + ADD or \
                perm == CHANGE + READ or \
                perm == CHANGE + ADD + DELETE or \
                perm == CHANGE + ADD + READ or \
                perm == CHANGE + READ + DELETE or \
                perm == CHANGE + ADD + DELETE + READ
    if pType == DELETE:
        return perm % 2 == 1
    return False


class AtlPermissionManager(models.Manager):

    def filter_for_object(self, object):
        ct = ContentType.objects.get_for_model(object)
        return self.get_query_set().filter(content_type=ct, object_id=object.id)        
    
class BaseAtlPermission(models.Model):
    codename = models.CharField(_('codename'), max_length=2)
    
    class Meta:
        abstract = True
        
    def can_add(self):
        return __get_permmision_value__(self.codename, ADD)
    
    def can_change(self):
        return __get_permmision_value__(self.codename, CHANGE)
    
    def can_delete(self):
        return __get_permmision_value__(self.codename, DELETE)
    
    def can_read(self):
        return __get_permmision_value__(self.codename, READ)     
            
        
class AtlPermission(BaseAtlPermission):
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=36)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    objects = AtlPermissionManager()

    class Meta:
        abstract = True
    
    def get_add_permission(self):
        return u"%s.add_%s" % (self.content_object._meta.app_label, self.content_object._meta.module_name)
    
    def get_change_permission(self):
        return u"%s.change_%s" % (self.content_object._meta.app_label, self.content_object._meta.module_name)
    
    def get_delete_permission(self):
        return u"%s.delete_%s" % (self.content_object._meta.app_label, self.content_object._meta.module_name)
    
    def get_read_permission(self):
        return u"%s.read_%s" % (self.content_object._meta.app_label, self.content_object._meta.module_name)
    
    def permissions(self):
        l = []
        if self.can_add():
            l.append(self.get_add_permission())
        if self.can_change():
            l.append(self.get_change_permission())
        if self.can_delete():
            l.append(self.get_delete_permission())
        if self.can_read():
            l.append(self.get_read_permission())
        return set(l)


class AtlUserPermission(AtlPermission):
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _('user-object permission')
        verbose_name_plural = _('user-object permissions')
        unique_together = (('content_type', 'object_id', 'user'),)
        ordering = ('content_type__app_label', 'content_type__model', 'user__username')
        
    def __unicode__(self):
        return u"%s | %s | %s | %s" % (
            unicode(self.content_type.app_label),
            unicode(self.content_type),
            unicode(self.object_id),
            unicode(self.user))
    
        
class AtlGroupPermission(AtlPermission):
    group = models.ForeignKey(Group)

    class Meta:
        verbose_name = _('group-object permission')
        verbose_name_plural = _('group-object permissions')
        unique_together = (('content_type', 'object_id', 'group'),)
        ordering = ('content_type__app_label', 'content_type__model', 'group__name')
        
    def __unicode__(self):
        return u"%s | %s | %s | %s" % (
            unicode(self.content_type.app_label),
            unicode(self.content_type),
            unicode(self.object_id),
            unicode(self.group))
        
def permissions_asignation(sender, instance, created, **kwargs):
    """
    """
    if created:
        if issubclass(sender, Node):
            container = instance.get_parent()
            if container is not None:
                try:
                    container_ct = ContentType.objects.get_for_model(container)
                    instance_ct = ContentType.objects.get_for_model(instance)
                    users = User.objects.filter(is_staff=True)
                    for user in users:
                        u_perms = AtlUserPermission.objects.filter(user=user, content_type=container_ct.id, object_id=container.id)
                        for u_perm in u_perms:
                            AtlUserPermission.objects.create(user=user, content_type=instance_ct, object_id=instance.id, codename=u_perm.codename)
                    groups = Group.objects.all()
                    for group in groups:
                        g_perms = AtlGroupPermission.objects.filter(group=group, content_type=container_ct.id, object_id=container.id)
                        for g_perm in g_perms:
                            AtlGroupPermission.objects.create(group=group, content_type=instance_ct, object_id=instance.id, codename=g_perm.codename)
                except (MultipleObjectsReturned, ObjectDoesNotExist):
                   pass
post_save.connect(permissions_asignation)

def permissions_elimination(sender, instance, **kwargs):
    """
    """
    if issubclass(sender, Node):
        instance_ct = ContentType.objects.get_for_model(instance)
        users = User.objects.filter(is_staff=True)
        for user in users:
            AtlUserPermission.objects.filter(user=user, content_type=instance_ct, object_id=instance.id).delete()
        groups = Group.objects.all()
        for group in groups:
            AtlGroupPermission.objects.filter(group=group, content_type=instance_ct, object_id=instance.id).delete()
pre_delete.connect(permissions_elimination)
   
def user_data_creation(sender, instance, created, **kwargs):
    everyone, is_created = Group.objects.get_or_create(name='Everyone') 
    if created:   
        instance.groups.add(everyone)
        instance.save()
#    elif instance.is_staff and instance.is_active:
#        creating the user default profile folders
#        folders = Folder.objects.get_or_create_user_default_folders(instance)
#        for folder, is_created in folders:
#            if is_created:
#                AtlUserPermission.objects.create(content_object=folder, user=instance, codename=unicode(ALL))
#                qs = AtlGroupPermission.objects.filter_for_object(folder).filter(group=everyone)
#                if qs:
#                    qs.delete()      
post_save.connect(user_data_creation, sender=User)
