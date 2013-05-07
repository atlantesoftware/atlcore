# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SiteProfile'
        db.create_table('siteprofile_siteprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['sites.Site'])),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('twitter', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('contact', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('logo_height', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('logo_width', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('favicon_height', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('favicon_width', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('favicon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('skin', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='site_profile', null=True, to=orm['skin.Skin'])),
        ))
        db.send_create_signal('siteprofile', ['SiteProfile'])


    def backwards(self, orm):
        
        # Deleting model 'SiteProfile'
        db.delete_table('siteprofile_siteprofile')


    models = {
        'siteprofile.siteprofile': {
            'Meta': {'object_name': 'SiteProfile'},
            'contact': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'favicon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'favicon_height': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'favicon_width': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'logo_height': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'logo_width': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['sites.Site']"}),
            'skin': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'site_profile'", 'null': 'True', 'to': "orm['skin.Skin']"}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'skin.skin': {
            'Meta': {'object_name': 'Skin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'skin_related'", 'symmetrical': 'False', 'to': "orm['skin.SkinType']"})
        },
        'skin.skintype': {
            'Meta': {'object_name': 'SkinType'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['siteprofile']
