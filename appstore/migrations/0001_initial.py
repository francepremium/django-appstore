# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AppCategory'
        db.create_table('appstore_appcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['appstore.AppCategory'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('appstore', ['AppCategory'])

        # Adding model 'AppFeature'
        db.create_table('appstore_appfeature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('appstore', ['AppFeature'])

        # Adding model 'App'
        db.create_table('appstore_app', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appstore.AppCategory'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('provides', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appstore.AppFeature'])),
            ('default_for_feature', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fork_of', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fork_set', null=True, to=orm['appstore.App'])),
        ))
        db.send_create_signal('appstore', ['App'])

        # Adding model 'AppVersion'
        db.create_table('appstore_appversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appstore.App'])),
            ('version', self.gf('django.db.models.fields.IntegerField')()),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('fork_of', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fork_set', null=True, to=orm['appstore.AppVersion'])),
        ))
        db.send_create_signal('appstore', ['AppVersion'])

        # Adding M2M table for field requires on 'AppVersion'
        db.create_table('appstore_appversion_requires', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('appversion', models.ForeignKey(orm['appstore.appversion'], null=False)),
            ('appfeature', models.ForeignKey(orm['appstore.appfeature'], null=False))
        ))
        db.create_unique('appstore_appversion_requires', ['appversion_id', 'appfeature_id'])

        # Adding model 'Environment'
        db.create_table('appstore_environment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('appstore', ['Environment'])

        # Adding M2M table for field appversions on 'Environment'
        db.create_table('appstore_environment_appversions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('environment', models.ForeignKey(orm['appstore.environment'], null=False)),
            ('appversion', models.ForeignKey(orm['appstore.appversion'], null=False))
        ))
        db.create_unique('appstore_environment_appversions', ['environment_id', 'appversion_id'])

        # Adding M2M table for field users on 'Environment'
        db.create_table('appstore_environment_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('environment', models.ForeignKey(orm['appstore.environment'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('appstore_environment_users', ['environment_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'AppCategory'
        db.delete_table('appstore_appcategory')

        # Deleting model 'AppFeature'
        db.delete_table('appstore_appfeature')

        # Deleting model 'App'
        db.delete_table('appstore_app')

        # Deleting model 'AppVersion'
        db.delete_table('appstore_appversion')

        # Removing M2M table for field requires on 'AppVersion'
        db.delete_table('appstore_appversion_requires')

        # Deleting model 'Environment'
        db.delete_table('appstore_environment')

        # Removing M2M table for field appversions on 'Environment'
        db.delete_table('appstore_environment_appversions')

        # Removing M2M table for field users on 'Environment'
        db.delete_table('appstore_environment_users')


    models = {
        'appstore.app': {
            'Meta': {'ordering': "('name',)", 'object_name': 'App'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['appstore.AppCategory']"}),
            'default_for_feature': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fork_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fork_set'", 'null': 'True', 'to': "orm['appstore.App']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'provides': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['appstore.AppFeature']"})
        },
        'appstore.appcategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AppCategory'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['appstore.AppCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'appstore.appfeature': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AppFeature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'appstore.appversion': {
            'Meta': {'ordering': "('app', 'version')", 'object_name': 'AppVersion'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['appstore.App']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'fork_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fork_set'", 'null': 'True', 'to': "orm['appstore.AppVersion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'requires': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['appstore.AppFeature']", 'symmetrical': 'False', 'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {})
        },
        'appstore.environment': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Environment'},
            'appversions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['appstore.AppVersion']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['appstore']