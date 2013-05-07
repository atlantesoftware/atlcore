# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SkinType'
        db.create_table('skin_skintype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('skin', ['SkinType'])

        # Adding model 'Skin'
        db.create_table('skin_skin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('skin', ['Skin'])

        # Adding M2M table for field type on 'Skin'
        db.create_table('skin_skin_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('skin', models.ForeignKey(orm['skin.skin'], null=False)),
            ('skintype', models.ForeignKey(orm['skin.skintype'], null=False))
        ))
        db.create_unique('skin_skin_type', ['skin_id', 'skintype_id'])


    def backwards(self, orm):
        
        # Deleting model 'SkinType'
        db.delete_table('skin_skintype')

        # Deleting model 'Skin'
        db.delete_table('skin_skin')

        # Removing M2M table for field type on 'Skin'
        db.delete_table('skin_skin_type')


    models = {
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

    complete_apps = ['skin']
