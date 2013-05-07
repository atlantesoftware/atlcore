# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Video.video_url'
        db.alter_column('contenttype_video', 'video_url', self.gf('django.db.models.fields.FilePathField')(path='/var/django/onu/onu/files/videosftp', max_length=256))

        # Changing field 'Video.thumbnail'
        db.alter_column('contenttype_video', 'thumbnail', self.gf('atlcore.libs.stdimage.fields.StdImageField')(name='thumbnail', thumbnail_size={'width': 100, 'force': True, 'height': 100}, max_length=100, size={'width': 640, 'force': None, 'height': 480}))


    def backwards(self, orm):
        
        # Changing field 'Video.video_url'
        db.alter_column('contenttype_video', 'video_url', self.gf('django.db.models.fields.FilePathField')(path='/home/ariel/workspaceHELIOS/sitv/files/videosftp', max_length=256))

        # Changing field 'Video.thumbnail'
        db.alter_column('contenttype_video', 'thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=256))


    models = {
        'aspect.aspect': {
            'Meta': {'object_name': 'Aspect'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
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
        'contenttype.audio': {
            'Meta': {'object_name': 'Audio', '_ormbases': ['contenttype.Content']},
            'audio': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contenttype.banner': {
            'Meta': {'object_name': 'Banner', '_ormbases': ['contenttype.Content']},
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'flash': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'obsolete_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'open_in_new_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resource_type': ('django.db.models.fields.CharField', [], {'default': "'Image'", 'max_length': '20'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
        'contenttype.document': {
            'Meta': {'object_name': 'Document', '_ormbases': ['contenttype.Content']},
            'body': ('django.db.models.fields.TextField', [], {}),
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'obsolete_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'contenttype.file': {
            'Meta': {'object_name': 'File', '_ormbases': ['contenttype.Content']},
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'contenttype.folder': {
            'Meta': {'object_name': 'Folder', '_ormbases': ['contenttype.Container']},
            'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Container']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contenttype.link': {
            'Meta': {'object_name': 'Link', '_ormbases': ['contenttype.Content']},
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': "'null'"}),
            'open_in_new_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'contenttype.map': {
            'Meta': {'object_name': 'Map', '_ormbases': ['contenttype.Content']},
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'embeded_map': ('django.db.models.fields.TextField', [], {})
        },
        'contenttype.news': {
            'Meta': {'object_name': 'News', '_ormbases': ['contenttype.Content']},
            'author_photo': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'obsolete_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'contenttype.node': {
            'Meta': {'object_name': 'Node'},
            'aspect': ('atlcore.aspect.fields.AtlAspectField', [], {'symmetrical': 'False', 'related_name': "'node_related'", 'blank': 'True', 'to': "orm['aspect.Aspect']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'node_contents'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'5a4baf3828ca11e2b6cdf0def1a2b2d8'", 'max_length': '36', 'primary_key': 'True'}),
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
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'contenttype.picture': {
            'Meta': {'object_name': 'Picture', '_ormbases': ['contenttype.Content']},
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contenttype.video': {
            'Meta': {'object_name': 'Video', '_ormbases': ['contenttype.Content']},
            'body': ('django.db.models.fields.TextField', [], {}),
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'embeded_video': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'thumbnail': ('atlcore.libs.stdimage.fields.StdImageField', [], {'name': "'thumbnail'", 'thumbnail_size': "{'width': 100, 'force': True, 'height': 100}", 'max_length': '100', 'blank': 'True', 'size': "{'width': 640, 'force': None, 'height': 480}"}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'video_source': ('django.db.models.fields.CharField', [], {'default': "'local'", 'max_length': '20'}),
            'video_url': ('django.db.models.fields.FilePathField', [], {'path': "'/var/django/onu/onu/files/videosftp'", 'max_length': '256', 'blank': 'True'}),
            'x_aspect_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_aspect_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['contenttype']
