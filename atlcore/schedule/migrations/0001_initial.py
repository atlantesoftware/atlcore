# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Calendar'
        db.create_table('schedule_calendar', (
            ('container_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Container'], unique=True, primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, db_index=True)),
            ('image', self.gf('atlcore.libs.stdimage.fields.StdImageField')(name='image', thumbnail_size={'width': 100, 'force': True, 'height': 100}, max_length=100, blank=True, size={'width': 640, 'force': None, 'height': 480})),
        ))
        db.send_create_signal('schedule', ['Calendar'])

        # Adding model 'Event'
        db.create_table('schedule_event', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2011, 9, 22))),
            ('start_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 26, 59, 503536))),
            ('end_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2011, 9, 22, 9, 26, 59, 503611), max_length=255, null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.TimeField')(default=datetime.time(9, 56, 59, 503681))),
            ('full_day', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('end_recurring_period', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('image', self.gf('atlcore.libs.stdimage.fields.StdImageField')(max_length=100, name='image', thumbnail_size={'width': 100, 'force': True, 'height': 100}, blank=True)),
            ('params', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('schedule', ['Event'])

        # Adding model 'Occurrence'
        db.create_table('schedule_occurrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('original_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('original_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Event'])),
        ))
        db.send_create_signal('schedule', ['Occurrence'])


    def backwards(self, orm):
        
        # Deleting model 'Calendar'
        db.delete_table('schedule_calendar')

        # Deleting model 'Event'
        db.delete_table('schedule_event')

        # Deleting model 'Occurrence'
        db.delete_table('schedule_occurrence')


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
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttype.container': {
            'Meta': {'object_name': 'Container', '_ormbases': ['contenttype.Content']},
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'ct_allowed': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'blank': 'True'})
        },
        'contenttype.content': {
            'Meta': {'object_name': 'Content', '_ormbases': ['contenttype.Node']},
            'contributor': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'coverage': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'creator': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'rights': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'})
        },
        'contenttype.node': {
            'Meta': {'object_name': 'Node'},
            'aspect': ('atlcore.aspect.fields.AtlAspectField', [], {'symmetrical': 'False', 'related_name': "'node_related'", 'blank': 'True', 'to': "orm['aspect.Aspect']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'node_contents'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'eea37528e52611e0bc840021708e5d56'", 'max_length': '36', 'primary_key': 'True'}),
            'image': ('atlcore.libs.stdimage.fields.StdImageField', [], {'name': "'image'", 'thumbnail_size': "{'width': 100, 'force': True, 'height': 100}", 'max_length': '100', 'blank': 'True', 'size': "{'width': 640, 'force': None, 'height': 480}"}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'es'", 'max_length': '5'}),
            'neutral': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'original_aspect': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'node_original_related'", 'blank': 'True', 'to': "orm['aspect.Aspect']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'node_owner'", 'null': 'True', 'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['contenttype.Container']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'node_related'", 'symmetrical': 'False', 'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'Public'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'schedule.calendar': {
            'Meta': {'object_name': 'Calendar'},
            'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Container']", 'unique': 'True', 'primary_key': True}),
            'image': ('atlcore.libs.stdimage.fields.StdImageField', [], {'name': "'image'", 'thumbnail_size': "{'width': 100, 'force': True, 'height': 100}", 'max_length': '100', 'blank': 'True', 'size': "{'width': 640, 'force': None, 'height': 480}"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'})
        },
        'schedule.event': {
            'Meta': {'object_name': 'Event'},
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': True}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2011, 9, 22, 9, 26, 59, 503611)', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_recurring_period': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 56, 59, 503681)'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'full_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'image': ('atlcore.libs.stdimage.fields.StdImageField', [], {'max_length': '100', 'name': "'image'", 'thumbnail_size': "{'width': 100, 'force': True, 'height': 100}", 'blank': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2011, 9, 22)'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(9, 26, 59, 503536)'})
        },
        'schedule.occurrence': {
            'Meta': {'object_name': 'Occurrence'},
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_end': ('django.db.models.fields.DateTimeField', [], {}),
            'original_start': ('django.db.models.fields.DateTimeField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['schedule']
