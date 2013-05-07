#coding=UTF-8
#from atlcore.settings import IMAGE_SIZE, THUMBNAIL_SIZE, LANGUAGES, LANGUAGE_CODE, DEFAULT_STATE, STATE_CHOICES
from atlcore.aspect.fields import AtlAspectField
from atlcore.aspect.models import Aspect
from atlcore.contenttype.manager import BaseManager
from atlcore.libs.stdimage import StdImageField
from django.db import models
from atlcore.utils.guid import get_guid


import copy
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from atlcore.utils.models import copy_model_instance
from atlcore.contenttype.manager import LocaleManager

IMAGE_SIZE = (640, 480)
THUMBNAIL_SIZE = (100, 100, True)
LANGUAGES = settings.LANGUAGES
LANGUAGE_CODE = 'es'
STATE_CHOICES = (('Public', _('Public')),('Private', _('Private')))
DEFAULT_STATE = STATE_CHOICES[0][0]


class Node(models.Model):
    PARENT_TYPES = ['contenttype.folder']
    
    # fields
    id = models.CharField(max_length=36, primary_key=True, default=get_guid)
    title = models.CharField(_('title'), max_length=256)
    slug = models.CharField(_('slug'), max_length=256, blank=True)
    description = models.TextField(_('description'), blank=True)
    meta_description = models.TextField(_('meta description'), blank=True)
    date=models.DateTimeField(_('date'), null=True, blank=True)
    update_date=models.DateTimeField(_('update date'), auto_now=True, editable=False, null=True)
    image = StdImageField(upload_to='nodes/images', blank=True, size=IMAGE_SIZE, thumbnail_size=THUMBNAIL_SIZE)
    language = models.CharField(_('language'), max_length=5, choices=LANGUAGES, default=LANGUAGE_CODE)
    neutral = models.BooleanField(_('Neutral'), blank=True)
    owner=models.ForeignKey(User, related_name='%(class)s_owner', verbose_name=_('owner'), blank=True, null=True)
    sites=models.ManyToManyField(Site, related_name='%(class)s_related', verbose_name=_('sites'))
    state=models.CharField(_('state'), max_length=20, choices=STATE_CHOICES, default=DEFAULT_STATE)
    view_count = models.IntegerField(_('view count'),default=0)
    
    created_on=models.DateTimeField(_('creation date'), auto_now_add=True, editable=False, null=True)
    updated_on=models.DateTimeField(_('update date'), auto_now=True, editable=False, null=True)
    
    
    # aspects relation
    aspect = AtlAspectField(Aspect, related_name='%(class)s_related', verbose_name=_('aspect'), blank=True)
    original_aspect = models.ManyToManyField(Aspect, related_name='%(class)s_original_related', verbose_name=_('original aspect'), blank=True)
        
    # container relation
    parent = models.ForeignKey('Container', related_name='children', blank=True, null=True)

    # content relation
    content_type = models.ForeignKey(ContentType, related_name='%(class)s_contents', blank=True, null=True, editable=False)
    order=models.PositiveIntegerField(editable=False, default=0, db_index=True)
    
    
    # managers    
    # default manager
    objects = BaseManager()  
    objects_translated = LocaleManager()
    
    class Meta:
        app_label = 'contenttype'
        
    def get_uuid(self):
        return uuid.uuid1()
        
        
#    def save(self):
#        if self.order == 0 : 
#            try: 
#                self.order = Node.objects.latest('order').order + 1
#            except:
#                self.order = 1
#        super(Node, self).save()
        
    def viewed(self):
        self.view_count += 1
        self.save()
    
    def get_ancestors(self):
        if self.parent:
            return self.parent.get_ancestors() + [self.get_parent()]
        return []        

    def __unicode__(self):
        return self.title
    
    def get_instance(self):
        if self.content_type:
            return self.content_type.get_object_for_this_type(pk=self.id)
        return self
    
    def get_parent(self):
        if self.parent:
            return self.parent.get_instance()
        return None
    
    def get_container_brothers(self):
        return Node.objects.filter(parent=self.parent)
    
    def admin_url(self):
        instance = self.get_instance()
        info = instance._meta.app_label, instance._meta.module_name
        return reverse('admin:%s_%s_details' % info, args=[self.id])    
    
    def admin_change_url(self):
        instance = self.get_instance()
        info = instance._meta.app_label, instance._meta.module_name
        return reverse('admin:%s_%s_change' % info, args=[self.id])  
    
    def admin_delete_url(self):
        instance = self.get_instance()
        info = instance._meta.app_label, instance._meta.module_name
        return reverse('admin:%s_%s_delete' % info, args=[self.id])   
    
    def admin_model_url(self):
        info=self._meta.app_label, self._meta.module_name
        return reverse('admin:%s_%s_changelist' % info)
    
    def cms_absolute_url(self):
        return '/%s/%s/%s' %(self.instance_class_name, self.id, self.slug)

    def get_absolute_url(self):
        if self.instance_class_name in ['link', 'banner', 'file']:
            return self.get_instance().get_absolute_url()
        else: 
            return reverse('%s_details' % self.instance_class_name, args=[self.id, self.slug])    
    
    def get_absolute_image_url(self):
        if self.image: 
            return "%s%s" % (settings.MEDIA_URL, self.image)
        if self.thumbnail:
            return "%s%s" % (settings.MEDIA_URL, self.thumbnail) 
        else:
            return None
              
    
    def image_absolute_url(self):
        if self.image:
            return "%s%s" % (settings.MEDIA_URL, self.image)
        if self.thumbnail:
            return "%s%s" % (settings.MEDIA_URL, self.thumbnail) 
    
    def get_image_path(self):
        if self.image:
            return self.image.path
        if self.thumbnail:
            return self.thumbnail.path
        
    def get_image_crop_path(self, width=128, height=128):
        if self.image:
            crop_url = self.get_image_crop(width, height)
            return "%s%s" % (settings.PROJECT_ROOT, crop_url)
        
     
    def get_meta(self):
        return self._meta
    
    def __get_instance_class_name(self):
        return str(self.content_type.model)
    class_name_instance = property(__get_instance_class_name) #Deprecated
    instance_class_name = property(__get_instance_class_name)
    
    def right_brother(self):
        brother = Node.objects.filter(parent__id=self.parent.id, order__lt=self.order).order_by('-order')
        print self.order
        if brother: 
            return brother[0].get_instance()
        else: 
            return self
    
    def left_brother(self):
        brother = Node.objects.filter(parent=self.parent, order__gt=self.order).order_by('order')
        if brother: 
            return brother[0].get_instance()
        else: 
            return self

    
    def get_image_thumbnail(self, width=128, height=128):
        from PIL import Image
        import os
        file_path, ext_path = os.path.splitext(self.get_image_path())
        file_absolute_url, ext_absolute_url = os.path.splitext(self.get_absolute_image_url())
        thumbnail_image_path = '%s_thumbnail_%sx%s%s' % (file_path, str(width), str(height), ext_path)
        thumbnail_image_absolute_url = '%s_thumbnail_%sx%s%s' % (file_absolute_url, str(width), str(height), ext_absolute_url)
        if not os.path.exists(thumbnail_image_path):
            try:
                image = Image.open(self.get_image_path())
                image.thumbnail((width, height), Image.ANTIALIAS)
                image.save(thumbnail_image_path)
            except:
                return ""
        return  thumbnail_image_absolute_url

    def get_image_crop(self, width=128, height=128):
        from PIL import Image
        import os
        if not self.image and not self.thumbnail: 
            return ''
        file_dir = os.path.dirname(self.get_image_path()) + '/thumbnails/'
        file_url_dir = os.path.dirname(self.get_absolute_image_url()) + '/thumbnails/' 
        file_name = os.path.basename(self.get_image_path())
        file_basename = file_name.split('.')[0]
        try:
            file_ext = file_name.split('.')[1]
        except:
            file_ext = ''
        thumbnail_image_path = '%s%s_%sx%s.%s' % (file_dir, file_basename, str(width), str(height), file_ext)
        thumbnail_image_absolute_url = '%s%s_%sx%s.%s' % (file_url_dir, file_basename, str(width), str(height), file_ext)
        
        if not os.path.exists(thumbnail_image_path):            
            image = Image.open(self.get_image_path())
    
            src_width, src_height = image.size
            src_ratio = float(src_width) / float(src_height)
            dst_width, dst_height = width, height
            dst_ratio = float(dst_width) / float(dst_height)
    
            if dst_ratio < src_ratio:
                crop_height = src_height
                crop_width = crop_height * dst_ratio
                x_offset = float(src_width - crop_width) / 2
                y_offset = 0
            else:
                crop_width = src_width
                crop_height = crop_width / dst_ratio
                x_offset = 0
                y_offset = float(src_height - crop_height) / 3
            image = image.crop((int(x_offset), int(y_offset), int(x_offset+crop_width), int(y_offset+crop_height)))
            image = image.resize((int(dst_width), int(dst_height)), Image.ANTIALIAS)
            try:
                image.save(thumbnail_image_path, image.format, quality=90, optimize=1)
            except:
                try:
                    if not os.path.exists(os.path.dirname(thumbnail_image_path)):
                        os.makedirs(os.path.dirname(thumbnail_image_path))
                    image.save(thumbnail_image_path, image.format, quality=90, optimize=1)
                except: 
                    try: 
                        image.save(thumbnail_image_path, image.format, quality=90)
                    except Exception, e:
                        return e
    
        return thumbnail_image_absolute_url



    def clone(self, parent, order=0):
        instance = self.get_instance()
        instance_duplicate = copy_model_instance(instance)
        instance_duplicate.parent = parent
        instance_duplicate.order = order    
        instance_duplicate.save()
        for field in instance._meta.many_to_many:
            source=getattr(instance, field.attname)
            destination=getattr(instance_duplicate, field.attname)
            for item in source.all():
                destination.add(item)
        return instance_duplicate


    def create_relation_methods(self):
        from atlcore.relations.models import AtlRelationsInstance
        r= AtlRelationsInstance.objects.relation_types_for_object2(self)
        slugs=[re.slug for re in r]
        for i in slugs:
            self.__setattr__('get_%s'%i, AtlRelationsInstance.objects.get_objects1_relation(self, i))
            self.__setattr__('get_first_%s'%i, AtlRelationsInstance.objects.get_first_objects1_relation(self, i))
            
    def get_relation_objects(self, relation_slug):
        '''
        Devuelve un listado de objetos relacionados con el objeto en cuestión pasándole como parámetro el slug de la relación.
        ''' 
        from atlcore.relations.models import AtlRelationsInstance
        return AtlRelationsInstance.objects.get_objects1_relation(self, relation_slug)()
