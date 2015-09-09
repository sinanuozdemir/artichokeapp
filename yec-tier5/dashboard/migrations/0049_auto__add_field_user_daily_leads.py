# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field target_market on 'Connection'
        m2m_table_name = db.shorten_name(u'dashboard_connection_target_market')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('connection', models.ForeignKey(orm[u'dashboard.connection'], null=False)),
            ('targetmarket', models.ForeignKey(orm[u'dashboard.targetmarket'], null=False))
        ))
        db.create_unique(m2m_table_name, ['connection_id', 'targetmarket_id'])

        # Adding field 'User.daily_leads'
        db.add_column(u'dashboard_user', 'daily_leads',
                      self.gf('django.db.models.fields.IntegerField')(default=0, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing M2M table for field target_market on 'Connection'
        db.delete_table(db.shorten_name(u'dashboard_connection_target_market'))

        # Deleting field 'User.daily_leads'
        db.delete_column(u'dashboard_user', 'daily_leads')


    models = {
        u'dashboard.apicredentials': {
            'Meta': {'object_name': 'apiCredentials'},
            'access_secret': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'access_token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'api_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'api_secret': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'social_media': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'})
        },
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
            'target_market': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.targetMarket']", 'null': 'True', 'blank': 'True'}),
            'used_for_stats': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.document': {
            'Meta': {'object_name': 'Document'},
            'analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'}),
            'date_competed': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 3, 0, 0)'}),
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'emails_new_to_user': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'emails_on_csv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'exported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_analyzed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'dashboard.statssnapshot': {
            'Meta': {'object_name': 'statsSnapshot'},
            'generated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 3, 0, 0)'}),
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
        u'dashboard.targetmarket': {
            'Meta': {'object_name': 'targetMarket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.user': {
            'Meta': {'object_name': 'User'},
            'available_for_stats': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'company_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'daily_leads': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'earned_onboarding_500': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'followed_tier5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'pricing_plan': ('django.db.models.fields.CharField', [], {'default': "'Free Plan'", 'max_length': '100', 'null': 'True'}),
            'referral_token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'referred': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'referred_by': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True'}),
            'tweeted_at_someone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter_access_token_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'twitter_access_token_secret': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'twitter_available_for_stats': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True'}),
            'twitter_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'twitter_oauth_token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1000', 'null': 'True'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'uploaded_a_csv': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'dashboard.website': {
            'Meta': {'object_name': 'Website'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 3, 0, 0)', 'null': 'True', 'blank': 'True'}),
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
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 3, 0, 0)'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['legion.Industry']", 'symmetrical': 'False'}),
            'is_analyzed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'klout_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_analyzed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'linkedin_bio': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_angellist': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True'}),
            'personal_crunchbase': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True'}),
            'personal_facebook': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True'}),
            'personal_github': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'personal_home_page': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'personal_linkedin': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True'}),
            'personal_twitter': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True'}),
            'personal_wikipedia': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'photo': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1000', 'null': 'True'}),
            'saved_photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'times_analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_bio': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'twitter_followers': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'twitter_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['dashboard']