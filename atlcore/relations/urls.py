from django.conf.urls.defaults import *

urlpatterns = patterns('atlcore.relations.views',
    url(r'^json_objects/(?P<model_list>.+)/$', 'json_objects', name='json-objects'),
)