#coding=UTF-8
from atlcore.contenttype.models.node import Node

from django.contrib.contenttypes.models import ContentType
 

def create_ct_relation(sender, instance, created, **kwargs):
    """
    """
    if created and issubclass(sender, Node):
        instance.content_type = ContentType.objects.get_for_model(instance)
        instance.save()
        
