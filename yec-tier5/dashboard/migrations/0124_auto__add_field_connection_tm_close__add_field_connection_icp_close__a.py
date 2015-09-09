# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Connection.tm_close'
        db.add_column(u'dashboard_connection', 'tm_close',
                      self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=6, decimal_places=4, blank=True),
                      keep_default=False)

        # Adding field 'Connection.icp_close'
        db.add_column(u'dashboard_connection', 'icp_close',
                      self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=6, decimal_places=4, blank=True),
                      keep_default=False)

        # Adding field 'Connection.user_close'
        db.add_column(u'dashboard_connection', 'user_close',
                      self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=6, decimal_places=4, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Connection.tm_close'
        db.delete_column(u'dashboard_connection', 'tm_close')

        # Deleting field 'Connection.icp_close'
        db.delete_column(u'dashboard_connection', 'icp_close')

        # Deleting field 'Connection.user_close'
        db.delete_column(u'dashboard_connection', 'user_close')


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
        u'dashboard.competitor': {
            'Meta': {'object_name': 'Competitor'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.keyWord']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.connection': {
            'Meta': {'object_name': 'Connection'},
            'angellist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'conversion_time_in_months': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'converted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'converted_on': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'crunchbase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'followed_by': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'followed_on': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'following': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'following_on': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'from_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icp_close': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '6', 'decimal_places': '4', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Job']", 'null': 'True', 'blank': 'True'}),
            'last_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)', 'null': 'True'}),
            'lead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lead_on': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'linkedin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'new_lead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num_companies': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'num_interests': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'num_locations': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'num_schools': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'num_titles': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'sourced_from': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.Document']", 'null': 'True', 'blank': 'True'}),
            'star_rating': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '6', 'decimal_places': '4', 'blank': 'True'}),
            'subscribed_to': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.Website']", 'null': 'True', 'blank': 'True'}),
            'target_market': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.targetMarket']", 'null': 'True', 'blank': 'True'}),
            'tm_close': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '6', 'decimal_places': '4', 'blank': 'True'}),
            'used_for_stats': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'}),
            'user_close': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '6', 'decimal_places': '4', 'blank': 'True'})
        },
        u'dashboard.document': {
            'Meta': {'object_name': 'Document'},
            'analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'}),
            'date_competed': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)'}),
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'emails_new_to_user': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'emails_on_csv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'exported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_analyzed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'dashboard.flag': {
            'Meta': {'object_name': 'flag'},
            'comments': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'flagEmail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flagFacebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flagJob': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flagLinkedin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flagOther': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flagPhone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flagTwitter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flag_on': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resolved': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'dashboard.icp': {
            'Meta': {'object_name': 'ICP'},
            'generated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)', 'null': 'True'}),
            'icp_dict': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'null': 'True'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'target_market': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.targetMarket']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.keyword': {
            'Meta': {'object_name': 'keyWord'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Tweet']", 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '170', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '170', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.marketevent': {
            'Meta': {'object_name': 'marketEvent'},
            'competitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Competitor']", 'null': 'True', 'blank': 'True'}),
            'date_ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)', 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'db_index': 'True'}),
            'followers_at_the_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'db_index': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Organization']", 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'sentiment_at_the_time': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'subscribers_at_the_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'type_of_event': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.message': {
            'Meta': {'object_name': 'Message'},
            'body': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Connection']", 'null': 'True', 'blank': 'True'}),
            'date_first_opened': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'type_of_message': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.messageview': {
            'Meta': {'object_name': 'MessageView'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Message']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.proxy': {
            'Meta': {'object_name': 'Proxy'},
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'null': 'True'}),
            'port': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True'}),
            'type_of_proxy': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True'})
        },
        u'dashboard.scraper': {
            'Meta': {'object_name': 'Scraper'},
            'current_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'last_run': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'targetmarket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.targetMarket']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'})
        },
        u'dashboard.statssnapshot': {
            'Meta': {'object_name': 'statsSnapshot'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']", 'null': 'True', 'blank': 'True'}),
            'competitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Competitor']", 'null': 'True', 'blank': 'True'}),
            'generated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_connections_used': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'period': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'stats': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'type_of_stats': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.targetmarket': {
            'Meta': {'object_name': 'targetMarket'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'query': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'star_limit': ('django.db.models.fields.DecimalField', [], {'default': '5', 'null': 'True', 'max_digits': '3', 'decimal_places': '1', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)', 'null': 'True'}),
            'favorite_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.keyWord']", 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'reply_to': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'retweet': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'retweet_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'status_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '170', 'null': 'True', 'blank': 'True'}),
            'textblob_sentiment': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'})
        },
        u'dashboard.twittersentiment': {
            'Meta': {'object_name': 'twitterSentiment'},
            'hours_looked_back': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyWord': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.keyWord']", 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'sentiment': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'time_taken': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)'}),
            'tweets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.Tweet']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.twitterstats': {
            'Meta': {'object_name': 'twitterStats'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']", 'null': 'True', 'blank': 'True'}),
            'competitor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Competitor']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_followers': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'num_following': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'time_taken': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.user': {
            'Meta': {'object_name': 'User'},
            'available_for_stats': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'company_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'competitors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['legion.Company']", 'null': 'True', 'through': u"orm['dashboard.Competitor']", 'blank': 'True'}),
            'daily_leads': ('django.db.models.fields.IntegerField', [], {'default': '5', 'null': 'True'}),
            'default_period': ('django.db.models.fields.CharField', [], {'default': "'45'", 'max_length': '5', 'null': 'True'}),
            'earned_onboarding_500': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'followed_tier5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'google_access_token': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'google_auth_email': ('django.db.models.fields.EmailField', [], {'null': 'True', 'default': 'None', 'max_length': '75', 'blank': 'True', 'unique': 'True', 'db_index': 'True'}),
            'google_refresh_token': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_token': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['legion.Industry']", 'symmetrical': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'linkedin_access_token': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'linkedin_access_token_expires': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'linkedin_public_profile': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'linkedin_secret_code': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            'mailchimp_access_token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'most_recent_follower_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Organization']", 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'password_token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'pricing_plan': ('django.db.models.fields.CharField', [], {'default': "'Free Plan'", 'max_length': '100', 'null': 'True'}),
            'referral_token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'referred': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'referred_by': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'settings_json': ('django.db.models.fields.TextField', [], {'default': '\'{"inbound_settings": {"toolbar": ["P.o.P Change","Total People","Negative Comments","Positive Comments", "Period (45 Days)"],"period": 45}}\'', 'null': 'True'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True'}),
            'tweeted_at_someone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter_access_token_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'twitter_access_token_secret': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'twitter_available_for_stats': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True'}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'twitter_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'twitter_oauth_token': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1000', 'null': 'True'}),
            'twitter_picture': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '500', 'null': 'True'}),
            'type_of_entity': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'null': 'True'}),
            'uploaded_a_csv': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'dashboard.website': {
            'Meta': {'object_name': 'Website'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'type_of_website': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'legion.company': {
            'Meta': {'object_name': 'Company'},
            'city': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'company_angellist': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'company_crunchbase': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'company_facebook': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'company_home_page': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'company_linkedin': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'company_twitter': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'company_wikipedia': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'date_aquired': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_founded': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_host': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email_pattern': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'funding': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['legion.Industry']", 'symmetrical': 'False', 'blank': 'True'}),
            'last_analyzed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'linkedin_bio': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'number_of_employees': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'revenue': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'times_analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'twitter_bio': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'})
        },
        u'legion.industry': {
            'Meta': {'object_name': 'Industry'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'legion.job': {
            'Meta': {'object_name': 'Job'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']"}),
            'date_ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'months': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'legion.person': {
            'Meta': {'object_name': 'Person'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 6, 0, 0)'}),
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
            'personal_google_plus': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True'}),
            'personal_home_page': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'personal_linkedin': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True'}),
            'personal_twitter': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True'}),
            'personal_wikipedia': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'photo': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1000', 'null': 'True'}),
            'saved_photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'times_analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_bio': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'twitter_followers': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'twitter_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['dashboard']