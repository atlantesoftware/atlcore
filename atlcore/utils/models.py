#coding=UTF-8
from django.db.models import AutoField

def copy_model_instance(obj):
    initial = dict([(f.name, getattr(obj, f.name))
                    for f in obj._meta.fields
                    if not isinstance(f, AutoField) and not f in obj._meta.parents.values() and f.name != 'id'])
    return obj.__class__(**initial)
