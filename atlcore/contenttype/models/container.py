#coding=UTF-8

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import ugettext as _

from atlcore.contenttype.models.content import Content, Node
from atlcore.contenttype.manager import LocaleManager

class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class Container(Content):
    
    _registry = {}
    
    ct_allowed = models.CommaSeparatedIntegerField(max_length=256, blank=True, editable=False)
    
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    def __init__(self, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)
        self._childrens = None
        #self.load_registry()
                
    def load_registry(self):
        if not self.ct_allowed:
            if self.parent:
                self.parent = self.parent.get_instance()
                if isinstance(self, self.parent.content_type.model_class()):
                    
                    if not self.parent._registry: 
                        self.parent.load_registry()
                    self._registry = self.parent._registry
                else:
                    self._registry = self.__class__._registry
                self.__push_to_db__()
        else:
            self.__pull_from_db__()
                
#    def save(self, *args, **kwargs):
#        super(Container, self).save(*args, **kwargs)
#        ct_allowed = ','.join([str(ContentType.objects.get_for_model(m[1]).id) for m in self._registry.items()])
#        if ct_allowed != self.ct_allowed:
#            self.ct_allowed = ct_allowed
#            self.save()      

    @classmethod    
    def get_container_items(self, aspect_slug, max=None):
        try:
            return Node.objects.filter(parent__aspect__slug = aspect_slug).order_by("-order")[:max]
        except IndexError:
            return []              
      
    @classmethod    
    def register(cls, model_or_iterable):
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(_('The model %s is abstract, so it cannot be registered in a Container.') % model.__name__)
            model_key = "%s__%s" %(model._meta.app_label, model._meta.module_name)
            if model_key in cls._registry:
                raise AlreadyRegistered(_('The model %s is already registered') % model.__name__)
            cls._registry[model_key] = model                             
        
    @classmethod        
    def unregister(cls, model_or_iterable):
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            model_key = "%s__%s" %(model._meta.app_label, model._meta.module_name)
            if model_key not in cls._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del cls._registry[model_key]
            
    @classmethod
    def unregister_all(cls):
        cls._registry = {}
        
    def __pull_from_db__(self):
        self._registry = {}     
        ids = self.ct_allowed.split(',')
        models = []
        for id in ids:
            try:
                model = ContentType.objects.get(pk=id).model_class()
            except:
                pass
            else:
                models.append(model)
        if models:
            self.iregister(models)
            
    def __push_to_db__(self):
        if self.id:
            if not self._registry:
                self.load_registry()
            self.ct_allowed = ','.join([str(ContentType.objects.get_for_model(m[1]).id) for m in self._registry.items()])        
            self.save()                  
        
    def iregister(self, model_or_iterable):
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(_('The model %s is abstract, so it cannot be registered in a Container.') % model.__name__)
            model_key = "%s__%s" %(model._meta.app_label, model._meta.module_name)
            if model_key in self._registry:
                raise AlreadyRegistered(_('The model %s is already registered') % model.__name__)
            self._registry[model_key] = model
        self.__push_to_db__()                           
        
    def iunregister(self, model_or_iterable):
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            model_key = "%s__%s" %(model._meta.app_label, model._meta.module_name)
            if model_key not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del self._registry[model_key]
        self.__push_to_db__()
            
    def iregister_all(self):
        self._registry = self.__class__._registry
        self.__push_to_db__()          
            
    def iunregister_all(self):
        self._registry = {}
    
    class Meta:
        app_label = 'contenttype'
        
    def admin_delete_selected(self):
        info=self._meta.app_label, self._meta.module_name
        return reverse('admin:%s_%s_delete_selected' % info, args=[self.id])    
    
    def __get_childrens(self):
        if self._childrens is None:
            self._childrens = self.get_childrens() 
        return self._childrens
        
    childrens = property(__get_childrens)
    
    def has_childrens(self):
        return self.childrens is not []

    def get_childrens(self, max=None, type=Content, order="-order"):
        return type.objects.filter(parent__id = self.id).order_by(order)[:max]

    
    def getChildren(self):
        """ Deprecated """
        return Content.objects.filter(parent__id = self.id).order_by("-order")
    
    def get_descendants(self):
        descendants = self.getChildren()
        for desc in descendants:
            if isinstance(desc, Container):
                descendants |= desc.get_descendants()
        return descendants
    
    def clone(self, parent, order=0):
        parent_duplicate = super(Container, self).clone(parent, order)
        contents = self.getChildren()
        for content in contents:
            content.get_instance().clone(parent_duplicate)
        return parent_duplicate
    