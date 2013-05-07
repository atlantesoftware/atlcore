# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ConfigValues'
        db.create_table('configvalues_configvalues', (
            ('id', self.gf('django.db.models.fields.CharField')(default='70cf301ee71f11e1a3800015af98de7d', max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('configvalues', ['ConfigValues'])


    def backwards(self, orm):
        
        # Deleting model 'ConfigValues'
        db.delete_table('configvalues_configvalues')


    models = {
        'configvalues.configvalues': {
            'Meta': {'object_name': 'ConfigValues'},
            'id': ('django.db.models.fields.CharField', [], {'default': "'70d030c2e71f11e1a3800015af98de7d'", 'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['configvalues']
