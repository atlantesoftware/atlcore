#coding=UTF-8
import os, sys
sys.path.insert(0, '/var/django/mysiteproject/mysite')
import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from atlcore.contenttype.models import Folder
from django.contrib.sites.models import Site
from django.test.utils import setup_test_environment, teardown_test_environment
from django.db import connection

class TestSiteApp(object):
    
    verbosity = 1
    interactive = True
    old_name = settings.DATABASES['default']['NAME']
    
    def setup(self):
        setup_test_environment()
        settings.DEBUG = False
        connection.creation.create_test_db(self.verbosity, autoclobber=not self.interactive)
        site = Site.objects.get(id=1)
        self.folder = Folder()
        self.folder.title = 'Test'
        self.folder.save()
        self.folder.sites.add(site)
        self.folder.save()
        
    def test_exist(self):
        self.folder = Folder.objects.filter(title='Test')
        assert self.folder
        
    def test_component_arquitecture(self):
        from atlcore.vcl.components import Component, DataProvider
        dataprovider = DataProvider()
        dataprovider.a = 2
        dataprovider.b = 3
        component = Component(data_provider)
        component.theme = 'test_theme'
        assert component.config
         
        
    def teardown(self):
        connection.creation.destroy_test_db(self.old_name, self.verbosity)
        teardown_test_environment()





#import unittest
#import os
#import sys
#sys.path.insert(0, '/var/django/mysiteproject/mysite/')
#import settings
#PROJECT_ROOT= os.path.dirname(settings.__file__)
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#sys.path.insert(0, PROJECT_ROOT[:PROJECT_ROOT.rfind('/')])
#sys.path.insert(0, PROJECT_ROOT)
#from django.test.utils import setup_test_environment, teardown_test_environment
#
#verbosity = 1
#interactive = True
#
#setup_test_environment()
#settings.DEBUG = False
#old_name = settings.DATABASES['default']['NAME']
#
#from django.db import connection
#connection.creation.create_test_db(verbosity, autoclobber=not interactive)
#
#class MyFuncTestCase(unittest.TestCase):
#    
#    def testBasic(self):
#        from atlcore.contenttype.models import Folder
#        from django.contrib.sites.models import Site
#        site = Site.objects.get(id=1)
#        folder = Folder()
#        folder.title = 'Test'
#        folder.save()
#        folder.sites.add(site)
#        folder.save()
#        folder = Folder.objects.filter(title='Test')
#        assert folder 
#
#
#    def testBasic2(self):
#        a = 2
#        b = 3
#        assert a + b == 5
#
#connection.creation.destroy_test_db(old_name, verbosity)
#teardown_test_environment()