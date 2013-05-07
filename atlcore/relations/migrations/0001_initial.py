# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AtlRelation'
        db.create_table('relations_atlrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=50, db_index=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('is_bidirectional', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('relations', ['AtlRelation'])

        # Adding M2M table for field content_types_group1 on 'AtlRelation'
        db.create_table('relations_atlrelation_content_types_group1', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('atlrelation', models.ForeignKey(orm['relations.atlrelation'], null=False)),
            ('contenttype', models.ForeignKey(orm['contenttypes.contenttype'], null=False))
        ))
        db.create_unique('relations_atlrelation_content_types_group1', ['atlrelation_id', 'contenttype_id'])

        # Adding M2M table for field content_types_group2 on 'AtlRelation'
        db.create_table('relations_atlrelation_content_types_group2', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('atlrelation', models.ForeignKey(orm['relations.atlrelation'], null=False)),
            ('contenttype', models.ForeignKey(orm['contenttypes.contenttype'], null=False))
        ))
        db.create_unique('relations_atlrelation_content_types_group2', ['atlrelation_id', 'contenttype_id'])

        # Adding model 'AtlRelationsInstance'
        db.create_table('relations_atlrelationsinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('relation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['relations.AtlRelation'])),
            ('object1_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('content_type1_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('object2_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('content_type2_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('relations', ['AtlRelationsInstance'])


    def backwards(self, orm):
        
        # Deleting model 'AtlRelation'
        db.delete_table('relations_atlrelation')

        # Removing M2M table for field content_types_group1 on 'AtlRelation'
        db.delete_table('relations_atlrelation_content_types_group1')

        # Removing M2M table for field content_types_group2 on 'AtlRelation'
        db.delete_table('relations_atlrelation_content_types_group2')

        # Deleting model 'AtlRelationsInstance'
        db.delete_table('relations_atlrelationsinstance')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'relations.atlrelation': {
            'Meta': {'object_name': 'AtlRelation'},
            'content_types_group1': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'atlrelation_instance1'", 'symmetrical': 'False', 'to': "orm['contenttypes.ContentType']"}),
            'content_types_group2': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'atlrelation_instance2'", 'symmetrical': 'False', 'to': "orm['contenttypes.ContentType']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_bidirectional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'relations.atlrelationsinstance': {
            'Meta': {'object_name': 'AtlRelationsInstance'},
            'content_type1_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'content_type2_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object1_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'object2_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['relations.AtlRelation']"})
        }
    }

    complete_apps = ['relations']
