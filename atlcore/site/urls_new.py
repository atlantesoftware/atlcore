from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
            url(r'^(?P<id>[a-fA-F0-9]{32})/$', 'atlcore.site.views.details_view', name='news_details2'),
            url(r'^(?P<id>[a-fA-F0-9]{32})/(?P<slug>[a-zA-Z0-9-]+)/$', 'atlcore.site.views.details_view', name='news_details'),
            #url(r'^(?P<slug>[a-zA-Z0-9-]+)/$', views.details_view, name='%s_details1' %self.opts.module_name),
            
            #url(r'^(?P<id>[a-fA-F0-9]{32})/(?P<slug>[a-zA-Z0-9-]+)/(?P<template_name>.+)/$', self.details_view, name='%s_details_with_view' %self.opts.module_name),
            #url(r'^ajax/(?P<id>[a-fA-F0-9]{32})/(?P<view_name>.+)/$', self.ajax_details_view, name='%s_ajax_details' %self.opts.module_name),
        )