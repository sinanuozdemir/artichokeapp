# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        

        # Adding field 'Person.linkedin_bio'
        db.add_column(u'legion_person', 'linkedin_bio',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True),
                      keep_default=False)

        # Adding field 'Person.twitter_bio'
        db.add_column(u'legion_person', 'twitter_bio',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True),
                      keep_default=False)

        # Adding unique constraint on 'Person', fields ['personal_github']
        db.create_unique(u'legion_person', ['personal_github'])


    def backwards(self, orm):
        # Removing unique constraint on 'Person', fields ['personal_github']
        db.delete_unique(u'legion_person', ['personal_github'])

        # Deleting field 'Person.linkedin_bio'
        db.delete_column(u'legion_person', 'linkedin_bio')

        # Deleting field 'Person.twitter_bio'
        db.delete_column(u'legion_person', 'twitter_bio')

        


    models = {
        u'legion.company': {
            'Meta': {'object_name': 'Company'},
            'company_angellist': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company_crunchbase': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company_facebook': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company_home_page': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company_linkedin': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company_twitter': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'company_wikipedia': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date_aquired': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_founded': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_host': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'email_pattern': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'funding': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['legion.Industry']", 'symmetrical': 'False', 'blank': 'True'}),
            'last_analyzed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'number_of_employees': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'revenue': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'times_analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'legion.education': {
            'Meta': {'object_name': 'Education'},
            'date_ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'education_level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fields_of_study': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['legion.Industry']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']"}),
            'school_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'legion.emailaddress': {
            'Meta': {'object_name': 'EmailAddress'},
            'address': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': 'None', 'max_length': '100', 'blank': 'True', 'unique': 'True', 'db_index': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deliverable': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 1, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'type_of_email': ('django.db.models.fields.CharField', [], {'max_length': '25'})
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
        u'legion.lead': {
            'Meta': {'object_name': 'Lead'},
            'date_matched': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 1, 0, 0)'}),
            'discovered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Organization']", 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']"})
        },
        u'legion.leadnote': {
            'Meta': {'object_name': 'LeadNote'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 1, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Lead']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True'})
        },
        u'legion.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_of_organization': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'legion.person': {
            'Meta': {'object_name': 'Person'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 1, 0, 0)'}),
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
            'photo': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1000', 'null': 'True'}),
            'saved_photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'times_analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_bio': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'twitter_followers': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'twitter_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'legion.query': {
            'Meta': {'ordering': "['-date_made']", 'object_name': 'Query'},
            'date_made': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 1, 0, 0)'}),
            'email_counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'emails_produced': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leads_produced': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'linkedin_counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'needs_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'needs_emails': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'needs_people': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Organization']", 'null': 'True'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['legion.Person']", 'symmetrical': 'False'}),
            'people_generated': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'people_produced': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'twitter_counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']"})
        },
        u'legion.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'max_leads_per_month': ('django.db.models.fields.IntegerField', [], {'default': '600'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'legion.userpermissions': {
            'Meta': {'object_name': 'UserPermissions'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_team_leader': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'linkedin_access_token': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'linkedin_code_expires_in': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 1, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'linkedin_secret_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_leads_per_month': ('django.db.models.fields.IntegerField', [], {'default': '500'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Organization']", 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.files.FileField', [], {'default': "'user_photos/no-img.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']"})
        }
    }

    complete_apps = ['legion']