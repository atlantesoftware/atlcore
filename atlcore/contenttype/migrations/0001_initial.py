# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Node'
        db.create_table('contenttype_node', (
            ('id', self.gf('django.db.models.fields.CharField')(default='08c3424ce52911e091af0021708e5d56', max_length=36, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('image', self.gf('atlcore.libs.stdimage.fields.StdImageField')(name='image', thumbnail_size={'width': 100, 'force': True, 'height': 100}, max_length=100, blank=True, size={'width': 640, 'force': None, 'height': 480})),
            ('language', self.gf('django.db.models.fields.CharField')(default='es', max_length=5)),
            ('neutral', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='node_owner', null=True, to=orm['auth.User'])),
            ('state', self.gf('django.db.models.fields.CharField')(default='Public', max_length=20)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['contenttype.Container'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='node_contents', null=True, to=orm['contenttypes.ContentType'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
        ))
        db.send_create_signal('contenttype', ['Node'])

        # Adding M2M table for field sites on 'Node'
        db.create_table('contenttype_node_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('node', models.ForeignKey(orm['contenttype.node'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('contenttype_node_sites', ['node_id', 'site_id'])

        # Adding M2M table for field aspect on 'Node'
        db.create_table('contenttype_node_aspect', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('node', models.ForeignKey(orm['contenttype.node'], null=False)),
            ('aspect', models.ForeignKey(orm['aspect.aspect'], null=False))
        ))
        db.create_unique('contenttype_node_aspect', ['node_id', 'aspect_id'])

        # Adding M2M table for field original_aspect on 'Node'
        db.create_table('contenttype_node_original_aspect', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('node', models.ForeignKey(orm['contenttype.node'], null=False)),
            ('aspect', models.ForeignKey(orm['aspect.aspect'], null=False))
        ))
        db.create_unique('contenttype_node_original_aspect', ['node_id', 'aspect_id'])

        # Adding model 'Content'
        db.create_table('contenttype_content', (
            ('node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Node'], unique=True, primary_key=True)),
            ('contributor', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
            ('coverage', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
            ('creator', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
            ('rights', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
        ))
        db.send_create_signal('contenttype', ['Content'])

        # Adding model 'Container'
        db.create_table('contenttype_container', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
            ('ct_allowed', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=256, blank=True)),
        ))
        db.send_create_signal('contenttype', ['Container'])

        # Adding model 'Folder'
        db.create_table('contenttype_folder', (
            ('container_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Container'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('contenttype', ['Folder'])

        # Adding model 'News'
        db.create_table('contenttype_news', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('obsolete_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('contenttype', ['News'])

        # Adding model 'Video'
        db.create_table('contenttype_video', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
            ('video', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('video_url', self.gf('django.db.models.fields.FilePathField')(path='/var/django/rtv/rtv/files/videosftp', max_length=256, blank=True)),
            ('external_url', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('video_source', self.gf('django.db.models.fields.CharField')(default='local', max_length=20)),
            ('embeded_video', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=256, blank=True)),
            ('x_aspect_ratio', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('y_aspect_ratio', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('contenttype', ['Video'])

        # Adding model 'Audio'
        db.create_table('contenttype_audio', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
            ('audio', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('contenttype', ['Audio'])

        # Adding model 'Banner'
        db.create_table('contenttype_banner', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('obsolete_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('resource_type', self.gf('django.db.models.fields.CharField')(default='Image', max_length=20)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('flash', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('open_in_new_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('contenttype', ['Banner'])

        # Adding model 'Document'
        db.create_table('contenttype_document', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('obsolete_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('contenttype', ['Document'])

        # Adding model 'File'
        db.create_table('contenttype_file', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('contenttype', ['File'])

        # Adding model 'Picture'
        db.create_table('contenttype_picture', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('contenttype', ['Picture'])

        # Adding model 'Link'
        db.create_table('contenttype_link', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank='null')),
            ('open_in_new_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('contenttype', ['Link'])

        # Adding model 'Map'
        db.create_table('contenttype_map', (
            ('content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contenttype.Content'], unique=True, primary_key=True)),
            ('embeded_map', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('contenttype', ['Map'])


    def backwards(self, orm):
        
        # Deleting model 'Node'
        db.delete_table('contenttype_node')

        # Removing M2M table for field sites on 'Node'
        db.delete_table('contenttype_node_sites')

        # Removing M2M table for field aspect on 'Node'
        db.delete_table('contenttype_node_aspect')

        # Removing M2M table for field original_aspect on 'Node'
        db.delete_table('contenttype_node_original_aspect')

        # Deleting model 'Content'
        db.delete_table('contenttype_content')

        # Deleting model 'Container'
        db.delete_table('contenttype_container')

        # Deleting model 'Folder'
        db.delete_table('contenttype_folder')

        # Deleting model 'News'
        db.delete_table('contenttype_news')

        # Deleting model 'Video'
        db.delete_table('contenttype_video')

        # Deleting model 'Audio'
        db.delete_table('contenttype_audio')

        # Deleting model 'Banner'
        db.delete_table('contenttype_banner')

        # Deleting model 'Document'
        db.delete_table('contenttype_document')

        # Deleting model 'File'
        db.delete_table('contenttype_file')

        # Deleting model 'Picture'
        db.delete_table('contenttype_picture')

        # Deleting model 'Link'
        db.delete_table('contenttype_link')

        # Deleting model 'Map'
        db.delete_table('contenttype_map')


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
            'id': ('django.db.models.fields.CharField', [], {'default': "'08d41630e52911e091af0021708e5d56'", 'max_length': '36', 'primary_key': 'True'}),
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
        'contenttype.picture': {
            'Meta': {'object_name': 'Picture', '_ormbases': ['contenttype.Content']},
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contenttype.video': {
            'Meta': {'object_name': 'Video', '_ormbases': ['contenttype.Content']},
            'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contenttype.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'embeded_video': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '256', 'blank': 'True'}),
            'video': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'video_source': ('django.db.models.fields.CharField', [], {'default': "'local'", 'max_length': '20'}),
            'video_url': ('django.db.models.fields.FilePathField', [], {'path': "'/var/django/rtv/rtv/files/videosftp'", 'max_length': '256', 'blank': 'True'}),
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
