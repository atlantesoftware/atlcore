# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Aspect'
        db.create_table('aspect_aspect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50, db_index=True, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('atlcore.aspect.fields.AtlAspectForeignKeyField')(blank=True, related_name='children', null=True, to=orm['aspect.Aspect'])),
        ))
        db.send_create_signal('aspect', ['Aspect'])

        # Adding M2M table for field sites on 'Aspect'
        db.create_table('aspect_aspect_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aspect', models.ForeignKey(orm['aspect.aspect'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('aspect_aspect_sites', ['aspect_id', 'site_id'])


    def backwards(self, orm):
        
        # Deleting model 'Aspect'
        db.delete_table('aspect_aspect')

        # Removing M2M table for field sites on 'Aspect'
        db.delete_table('aspect_aspect_sites')


    models = {
        'aspect.aspect': {
            'Meta': {'object_name': 'Aspect'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'parent': ('atlcore.aspect.fields.AtlAspectForeignKeyField', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['aspect.Aspect']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'aspect_related'", 'symmetrical': 'False', 'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['aspect']
