from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext as _

from atlcore import settings as atlante_settings
from atlcore.contenttype.admin.base import Base
from atlcore.contenttype.models import Folder
from atlcore.schedule.models import Calendar, Event

use_tinymce = False
if 'tinymce' in settings.INSTALLED_APPS:
    from tinymce.widgets import TinyMCE
    use_tinymce = True

class CalendarAdmin(Base):
    pass


class EventAdmin(Base):
    
    add_form_template = '%s/%s/templates/admin/%s/%s/add.html' %(atlante_settings.DIRECTORY, Event._meta.app_label, Event._meta.app_label, Event._meta.module_name)
    change_form_template = '%s/%s/templates/admin/%s/%s/change.html' %(atlante_settings.DIRECTORY, Event._meta.app_label, Event._meta.app_label, Event._meta.module_name)

    fields = ('title', 'slug', 'description', 'image', 'start_date', 'start_time', 'end_time', 'end_date', 'full_day', 'end_recurring_period', 'frequency', 'parent', 'params')
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if use_tinymce and (db_field.name == 'description'):
            return db_field.formfield(widget=TinyMCE(attrs={'cols': 100, 'rows': 40},))
        return super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)
    

admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Event, EventAdmin)

Calendar.register(Event)
Folder.register(Calendar)