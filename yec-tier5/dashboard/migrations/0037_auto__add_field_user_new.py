# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.new'
        db.add_column(u'dashboard_user', 'new',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.new'
        db.delete_column(u'dashboard_user', 'new')


    models = {
        u'dashboard.connection': {
            'Meta': {'object_name': 'Connection'},
            'angellist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crunchbase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'followed_by': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'following': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'from_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'linkedin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'sourced_from': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.Document']", 'null': 'True', 'blank': 'True'}),
            'subscribed_to': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.Website']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.document': {
            'Meta': {'object_name': 'Document'},
            'analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'}),
            'date_competed': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 4, 0, 0)'}),
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'emails_new_to_user': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'emails_on_csv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'exported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_analyzed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'dashboard.statssnapshot': {
            'Meta': {'object_name': 'statsSnapshot'},
            'generated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 4, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_file_uploaded': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'number_of_analyzed_documents': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'number_of_connections_left': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'number_of_connections_used': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'number_of_extra_connections': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'server_state': ('django.db.models.fields.CharField', [], {'default': "'OK'", 'max_length': '25', 'null': 'True'}),
            'stats': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.user': {
            'Meta': {'object_name': 'User'},
            'available_for_stats': ('django.db.models.fields.IntegerField', [], {'default': '10000'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'most_recent_follower_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'password_token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True'}),
            'twitter_access_token_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'twitter_access_token_secret': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'twitter_available_for_stats': ('django.db.models.fields.IntegerField', [], {'default': '10000', 'null': 'True'}),
            'twitter_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'})
        },
        u'dashboard.website': {
            'Meta': {'object_name': 'Website'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 4, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'type_of_website': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'legion.industry': {
            'Meta': {'object_name': 'Industry'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'legion.person': {
            'Meta': {'object_name': 'Person'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 4, 0, 0)'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['legion.Industry']", 'symmetrical': 'False'}),
            'is_analyzed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'klout_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_analyzed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_angellist': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'personal_crunchbase': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'personal_facebook': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'personal_github': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'personal_home_page': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'personal_linkedin': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'personal_twitter': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'personal_wikipedia': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'photo': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1000', 'null': 'True'}),
            'saved_photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'times_analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['dashboard']