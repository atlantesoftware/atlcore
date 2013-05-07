#coding=UTF-8

from django.db.models.signals import pre_save
from atlcore.contenttype.models import Node


def update_node_order(sender, instance, **kwargs):
    if isinstance(instance, Node):
        if instance.order == 0 : 
            try: 
                instance.order = Node.objects.latest('order').order + 1
                instance.save()
            except:
                instance.order = 1
pre_save.connect(update_node_order)


    
