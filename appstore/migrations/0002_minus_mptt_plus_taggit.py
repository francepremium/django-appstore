# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AppCategory.lft'
        db.delete_column('appstore_appcategory', 'lft')

        # Deleting field 'AppCategory.parent'
        db.delete_column('appstore_appcategory', 'parent_id')

        # Deleting field 'AppCategory.level'
        db.delete_column('appstore_appcategory', 'level')

        # Deleting field 'AppCategory.tree_id'
        db.delete_column('appstore_appcategory', 'tree_id')

        # Deleting field 'AppCategory.rght'
        db.delete_column('appstore_appcategory', 'rght')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'AppCategory.lft'
        raise RuntimeError("Cannot reverse this migration. 'AppCategory.lft' and its values cannot be restored.")
        # Adding field 'AppCategory.parent'
        db.add_column('appstore_appcategory', 'parent',
                      self.gf('mptt.fields.TreeForeignKey')(related_name='children', null=True, to=orm['appstore.AppCategory'], blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AppCategory.level'
        raise RuntimeError("Cannot reverse this migration. 'AppCategory.level' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AppCategory.tree_id'
        raise RuntimeError("Cannot reverse this migration. 'AppCategory.tree_id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'AppCategory.rght'
        raise RuntimeError("Cannot reverse this migration. 'AppCategory.rght' and its values cannot be restored.")

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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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