from django.conf.urls.defaults import *

urlpatterns = patterns('atlcore.aspect.views',
    url(r'^list_aspects/$', 'list_aspect', name='root-aspects'),
    url(r'^list_aspects/(?P<parent_id>[a-fA-F0-9]+)/$', 'list_aspect', name='children-aspects'),
)