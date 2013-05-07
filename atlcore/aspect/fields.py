#coding=UTF-8
from atlcore.aspect.widgets import AtlAspectWidget, AtlAspectForeignKeyWidget

from django.conf import settings
from django.db.models import ManyToManyField, ForeignKey

class AtlAspectField(ManyToManyField):
    
    def formfield(self, **kwargs):
        defaults = {
            'widget': AtlAspectWidget(),
            'help_text': ''
        }
        defaults.update(kwargs)
        return super(AtlAspectField, self).formfield(**defaults)
 
    
class AtlAspectForeignKeyField(ForeignKey):
    
    def formfield(self, **kwargs):
        defaults = {
            'widget': AtlAspectForeignKeyWidget(),
        }
        defaults.update(kwargs)
        return super(AtlAspectForeignKeyField, self).formfield(**defaults)
    
if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^atlcore\.aspect\.fields\.AtlAspectField"])
    add_introspection_rules([], ["^atlcore\.aspect\.fields\.AtlAspectForeignKeyField"])
    