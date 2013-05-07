#coding=UTF-8
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from atlcore.relations import helper

class AtlRelationManager(models.Manager):
    """
    """
    
    def for_this_class(self, cls):
        qs = self.get_query_set()
        rel_types = []
        for rel_t in qs:
            if issubclass(cls, rel_t.models_in_group2) or (rel_t.is_bidirectional and issubclass(cls, rel_t.models_in_group1)):
                rel_types.append(rel_t)
        return rel_types
    
    def for_this_class_with_pos(self, cls):
        qs = self.for_this_class(cls)
        rel_types = []
        for rel_t in qs:
            if issubclass(cls, rel_t.models_in_group2):
                rel_types.append((rel_t, 2))
            elif rel_t.is_bidirectional and issubclass(cls, rel_t.models_in_group1):
                rel_types.append((rel_t, 1))
        return rel_types
    

class AtlRelation(models.Model):
    """
    Se utiliza para definir la semántica de una realación entre dos AtlNodes
    """
    
    title=models.CharField(_('title'), max_length=256,)
    slug = models.SlugField(_('slug'), default='', blank=True)
    description=models.TextField(_('description'))
    is_bidirectional=models.BooleanField(_('is bidirectional'), default=False)
    content_types_group1=models.ManyToManyField(ContentType, related_name='%(class)s_instance1', limit_choices_to=helper.Q())
    content_types_group2=models.ManyToManyField(ContentType, related_name='%(class)s_instance2', limit_choices_to=helper.Q())
    
    objects = AtlRelationManager()
    
    def get_meta(self):
        return self._meta

    def __unicode__(self):
        return self.title
    
    @property
    def models_in_group1(self):
        return tuple([ct.model_class() for ct in self.content_types_group1.all()])
    
    @property
    def models_in_group2(self):
        return tuple([ct.model_class() for ct in self.content_types_group2.all()])
    
    class Meta:
        verbose_name = ugettext('relation type')
        verbose_name_plural = ugettext('relation types')
    
    
class AtlRelationsInstanceManager(models.Manager):
    """
    """
    
    def for_this_object(self, obj):
        queryset = self.get_query_set()
        ct_id = ContentType.objects.get_for_model(obj).id
        qs1 = queryset.filter(content_type1_id = ct_id, object1_id = obj.id)
        qs2 = queryset.filter(content_type2_id = ct_id, object2_id = obj.id)
        return qs1|qs2
    
    def for_this_object_with_pos(self, obj):
        qs = self.for_this_object(obj)
        ct_id = ContentType.objects.get_for_model(obj).id
        rels = []
        for rel in qs:
            if rel.content_type2_id==ct_id and rel.object2_id == obj.id:
                rels.append((rel, 2))
            elif rel.content_type1_id==ct_id and rel.object1_id == obj.id:
                rels.append((rel, 1))
        return rels
    
    def get_objects1_relation(self, obj, slug):
        queryset = self.get_query_set().filter(relation__slug=slug)
        ct_id = ContentType.objects.get_for_model(obj).id
        qs1 = queryset.filter(content_type2_id = ct_id, object2_id = obj.id).values_list('content_type1_id', 'object1_id')
        qs2 = queryset.filter(content_type1_id = ct_id, object1_id = obj.id, relation__is_bidirectional=True).values_list('content_type2_id', 'object2_id')
        qs = list(qs1) + list(qs2)
        l = []
        for ct, id in qs:
            try:
                ctype = ContentType.objects.get(pk=ct)
                obj = ctype.get_object_for_this_type(pk=id)
                l.append(obj)
            except (MultipleObjectsReturned, ObjectDoesNotExist):
                pass
        return lambda : l

    def get_first_objects1_relation(self, obj, slug, order_by='-order'):
        queryset = self.get_query_set().filter(relation__slug=slug)
        ct_id = ContentType.objects.get_for_model(obj).id
        qs1 = queryset.filter(content_type2_id = ct_id, object2_id = obj.id).values_list('content_type1_id', 'object1_id')
        qs2 = queryset.filter(content_type1_id = ct_id, object1_id = obj.id, relation__is_bidirectional=True).values_list('content_type2_id', 'object2_id')
        qs = list(qs1) + list(qs2)
        l = []
        for ct, id in qs:
            try:
                ctype = ContentType.objects.get(pk=ct)
                obj = ctype.get_object_for_this_type(pk=id)
                l.append(obj)
            except (MultipleObjectsReturned, ObjectDoesNotExist):
                pass
        return lambda : l[0]

    
    def relation_types_for_this_object(self, obj):
        relation_types = AtlRelation.objects.for_this_class(obj.__class__)
        queryset = self.get_query_set()
        ct_id = ContentType.objects.get_for_model(obj).id
        rts = []
        for rt in relation_types:
            qs = queryset.filter(content_type1_id = ct_id, object1_id = obj.id, relation__pk=rt.id)
            qs |= queryset.filter(content_type2_id = ct_id, object2_id = obj.id, relation__pk=rt.id)
            if qs: rts.append(rt)
        return rts
    
    def relation_types_for_object2(self, obj):
        relation_types = AtlRelation.objects.for_this_class(obj.__class__)
        queryset = self.get_query_set()
        ct_id = ContentType.objects.get_for_model(obj).id
        rts = []
        for rt in relation_types:
            qs = queryset.filter(content_type2_id = ct_id, object2_id = obj.id, relation__pk=rt.id)
            if qs:
                rts.append(rt)
            elif rt.is_bidirectional:
                qs = queryset.filter(content_type1_id = ct_id, object1_id = obj.id, relation__pk=rt.id)
                if qs:
                    rts.append(rt)
        return rts
    
    def new(self, relation, object1, object2):
        queryset = self.get_query_set()
        ct1 = ContentType.objects.get_for_model(object1).id
        ct2 = ContentType.objects.get_for_model(object2).id
        instance_dict = {
            'relation':relation,
            'object1_id':object1.id,
            'object2_id':object2.id,
            'content_type1_id':ct1,
            'content_type2_id':ct2,
        }
        return queryset.create(**instance_dict)


class AtlRelationsInstance(models.Model):
    """
    
    """
    
    relation = models.ForeignKey(AtlRelation)
    object1_id = models.CharField(_('object 1'), max_length=36)
    content_type1_id = models.PositiveIntegerField(_('content type 1'))
    object2_id = models.CharField(_('object 2'), max_length=36)
    content_type2_id = models.PositiveIntegerField(_('content type 2'))
    
    objects = AtlRelationsInstanceManager()
    
    class Meta:
        verbose_name = ugettext('relation')
        verbose_name_plural = ugettext('relations')
        
#    @property
#    def title(self):
#        return self.relation.title
    
    def __unicode__(self):
        return u"%s %s %s %s %s" %(self.object1, ugettext("is"), self.relation, ugettext("of"), self.object2)
    
    def get_meta(self):
        return self._meta
    
    def __get_model__(self, use_first=True):
        ct_id = self.content_type1_id if use_first else self.content_type2_id
        try:
            return ContentType.objects.get(pk=ct_id).model_class()
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            return None
    
    def __get_object__(self, use_first=True):
        model = self.__get_model__(use_first)
        id = self.object1_id if use_first else self.object2_id
        if model is not None:
            try:
                return model.objects.get(pk=id)
            except (MultipleObjectsReturned, ObjectDoesNotExist):
                pass
        return None        
        
    @property
    def model1(self):
        return self.__get_model__(use_first=True)
        
    @property
    def model2(self):
        return self.__get_model__(use_first=False)
   
    @property
    def object1(self):
        return self.__get_object__(use_first=True)
        
    @property
    def object2(self):
        return self.__get_object__(use_first=False)
    
    def admin_url(self):
        info=self._meta.app_label, self._meta.module_name
        return reverse('admin:%s_%s_change' % info, args=[self.id])        
    


        