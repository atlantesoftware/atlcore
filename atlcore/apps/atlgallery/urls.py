__author__ = 'hailem'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^folder/(?P<id>[a-fA-F0-9]{32})/$', 'atlgallery.views.image_list_view', name='image_list'),
    url(r'^folder/(?P<id>[a-fA-F0-9]{32})/(?P<slug>[a-zA-Z0-9-]+)/$', 'atlgallery.views.image_list_view', name='image_list_with_slug'),
)