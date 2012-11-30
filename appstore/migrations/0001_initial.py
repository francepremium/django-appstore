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
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appstore.AppCategory'], null=True, blank=True)),
            ('in_appstore', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('provides', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='provided_by', null=True, to=orm['appstore.AppFeature'])),
            ('default_for_feature', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('superseeds', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='superseeded_by', null=True, to=orm['appstore.App'])),
            ('deployed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('editor', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('appstore', ['App'])

        # Adding M2M table for field requires on 'App'
        db.create_table('appstore_app_requires', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('app', models.ForeignKey(orm['appstore.app'], null=False)),
            ('appfeature', models.ForeignKey(orm['appstore.appfeature'], null=False))
        ))
        db.create_unique('appstore_app_requires', ['app_id', 'appfeature_id'])

        # Adding model 'Environment'
        db.create_table('appstore_environment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('appstore', ['Environment'])

        # Adding M2M table for field apps on 'Environment'
        db.create_table('appstore_environment_apps', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('environment', models.ForeignKey(orm['appstore.environment'], null=False)),
            ('app', models.ForeignKey(orm['appstore.app'], null=False))
        ))
        db.create_unique('appstore_environment_apps', ['environment_id', 'app_id'])

        # Adding model 'UserEnvironment'
        db.create_table('appstore_userenvironment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('environment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appstore.Environment'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('appstore', ['UserEnvironment'])


    def backwards(self, orm):
        # Deleting model 'AppCategory'
        db.delete_table('appstore_appcategory')

        # Deleting model 'AppFeature'
        db.delete_table('appstore_appfeature')

        # Deleting model 'App'
        db.delete_table('appstore_app')

        # Removing M2M table for field requires on 'App'
        db.delete_table('appstore_app_requires')

        # Deleting model 'Environment'
        db.delete_table('appstore_environment')

        # Removing M2M table for field apps on 'Environment'
        db.delete_table('appstore_environment_apps')

        # Deleting model 'UserEnvironment'
        db.delete_table('appstore_userenvironment')


    models = {
        'appstore.app': {
            'Meta': {'ordering': "('name',)", 'object_name': 'App'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['appstore.AppCategory']", 'null': 'True', 'blank': 'True'}),
            'default_for_feature': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deployed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'in_appstore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'provides': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'provided_by'", 'null': 'True', 'to': "orm['appstore.AppFeature']"}),
            'requires': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'required_by'", 'blank': 'True', 'to': "orm['appstore.AppFeature']"}),
            'superseeds': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'superseeded_by'", 'null': 'True', 'to': "orm['appstore.App']"})
        },
        'appstore.appcategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AppCategory'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'appstore.appfeature': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AppFeature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'appstore.environment': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Environment'},
            'apps': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['appstore.App']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['appstore.UserEnvironment']", 'symmetrical': 'False'})
        },
        'appstore.userenvironment': {
            'Meta': {'ordering': "('creation_datetime',)", 'object_name': 'UserEnvironment'},
            'creation_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['appstore.Environment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['appstore']