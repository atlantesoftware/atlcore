# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Workflow'
        db.create_table('workflows_workflow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('initial_state', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='workflow_initial_state', null=True, to=orm['workflows.State'])),
            ('public_state', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='workflow_public_state', null=True, to=orm['workflows.State'])),
        ))
        db.send_create_signal('workflows', ['Workflow'])

        # Adding model 'State'
        db.create_table('workflows_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(related_name='states', to=orm['workflows.Workflow'])),
        ))
        db.send_create_signal('workflows', ['State'])

        # Adding M2M table for field transitions on 'State'
        db.create_table('workflows_state_transitions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('state', models.ForeignKey(orm['workflows.state'], null=False)),
            ('transition', models.ForeignKey(orm['workflows.transition'], null=False))
        ))
        db.create_unique('workflows_state_transitions', ['state_id', 'transition_id'])

        # Adding model 'AtlOwnerStatePermission'
        db.create_table('workflows_atlownerstatepermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.State'])),
        ))
        db.send_create_signal('workflows', ['AtlOwnerStatePermission'])

        # Adding model 'AtlUserStatePermission'
        db.create_table('workflows_atluserstatepermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.State'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('workflows', ['AtlUserStatePermission'])

        # Adding model 'AtlGroupStatePermission'
        db.create_table('workflows_atlgroupstatepermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.State'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
        ))
        db.send_create_signal('workflows', ['AtlGroupStatePermission'])

        # Adding model 'Transition'
        db.create_table('workflows_transition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.Workflow'])),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='destination_state', to=orm['workflows.State'])),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('workflows', ['Transition'])

        # Adding model 'StateObjectRelation'
        db.create_table('workflows_stateobjectrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='state_object', null=True, to=orm['contenttypes.ContentType'])),
            ('content_id', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.State'])),
        ))
        db.send_create_signal('workflows', ['StateObjectRelation'])

        # Adding unique constraint on 'StateObjectRelation', fields ['content_type', 'content_id', 'state']
        db.create_unique('workflows_stateobjectrelation', ['content_type_id', 'content_id', 'state_id'])

        # Adding model 'WorkflowObjectRelation'
        db.create_table('workflows_workflowobjectrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='workflow_object', null=True, to=orm['contenttypes.ContentType'])),
            ('content_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.Workflow'])),
        ))
        db.send_create_signal('workflows', ['WorkflowObjectRelation'])

        # Adding unique constraint on 'WorkflowObjectRelation', fields ['content_type', 'content_id']
        db.create_unique('workflows_workflowobjectrelation', ['content_type_id', 'content_id'])

        # Adding model 'WorkflowModelRelation'
        db.create_table('workflows_workflowmodelrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], unique=True)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflows.Workflow'])),
        ))
        db.send_create_signal('workflows', ['WorkflowModelRelation'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'WorkflowObjectRelation', fields ['content_type', 'content_id']
        db.delete_unique('workflows_workflowobjectrelation', ['content_type_id', 'content_id'])

        # Removing unique constraint on 'StateObjectRelation', fields ['content_type', 'content_id', 'state']
        db.delete_unique('workflows_stateobjectrelation', ['content_type_id', 'content_id', 'state_id'])

        # Deleting model 'Workflow'
        db.delete_table('workflows_workflow')

        # Deleting model 'State'
        db.delete_table('workflows_state')

        # Removing M2M table for field transitions on 'State'
        db.delete_table('workflows_state_transitions')

        # Deleting model 'AtlOwnerStatePermission'
        db.delete_table('workflows_atlownerstatepermission')

        # Deleting model 'AtlUserStatePermission'
        db.delete_table('workflows_atluserstatepermission')

        # Deleting model 'AtlGroupStatePermission'
        db.delete_table('workflows_atlgroupstatepermission')

        # Deleting model 'Transition'
        db.delete_table('workflows_transition')

        # Deleting model 'StateObjectRelation'
        db.delete_table('workflows_stateobjectrelation')

        # Deleting model 'WorkflowObjectRelation'
        db.delete_table('workflows_workflowobjectrelation')

        # Deleting model 'WorkflowModelRelation'
        db.delete_table('workflows_workflowmodelrelation')


    models = {
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'workflows.atlgroupstatepermission': {
            'Meta': {'object_name': 'AtlGroupStatePermission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.State']"})
        },
        'workflows.atlownerstatepermission': {
            'Meta': {'object_name': 'AtlOwnerStatePermission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.State']"})
        },
        'workflows.atluserstatepermission': {
            'Meta': {'object_name': 'AtlUserStatePermission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.State']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'workflows.state': {
            'Meta': {'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'transitions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'states'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['workflows.Transition']"}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'states'", 'to': "orm['workflows.Workflow']"})
        },
        'workflows.stateobjectrelation': {
            'Meta': {'unique_together': "(('content_type', 'content_id', 'state'),)", 'object_name': 'StateObjectRelation'},
            'content_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'state_object'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.State']"})
        },
        'workflows.transition': {
            'Meta': {'object_name': 'Transition'},
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destination_state'", 'to': "orm['workflows.State']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.Workflow']"})
        },
        'workflows.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workflow_initial_state'", 'null': 'True', 'to': "orm['workflows.State']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'public_state': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workflow_public_state'", 'null': 'True', 'to': "orm['workflows.State']"})
        },
        'workflows.workflowmodelrelation': {
            'Meta': {'object_name': 'WorkflowModelRelation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.Workflow']"})
        },
        'workflows.workflowobjectrelation': {
            'Meta': {'unique_together': "(('content_type', 'content_id'),)", 'object_name': 'WorkflowObjectRelation'},
            'content_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workflow_object'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['workflows.Workflow']"})
        }
    }

    complete_apps = ['workflows']
