# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.state'
        db.add_column(u'legion_person', 'state',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True),
                      keep_default=False)

        # Adding field 'Company.state'
        db.add_column(u'legion_company', 'state',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.state'
        db.delete_column(u'legion_person', 'state')

        # Deleting field 'Company.state'
        db.delete_column(u'legion_company', 'state')


    models = {
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
            'last_analyzed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'number_of_employees': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'revenue': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
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
            'email_pattern': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deliverable': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 8, 7, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
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
            'date_matched': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 8, 7, 0, 0)'}),
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
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 8, 7, 0, 0)'}),
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
            'city': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 8, 7, 0, 0)'}),
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
        },
        u'legion.query': {
            'Meta': {'ordering': "['-date_made']", 'object_name': 'Query'},
            'date_made': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 8, 7, 0, 0)'}),
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
        u'legion.script': {
            'Meta': {'object_name': 'script'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            'type_of_script': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'legion.techcomp': {
            'Meta': {'object_name': 'techComp'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']"}),
            'date_found': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 8, 7, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'date_stopped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'technology': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Technology']"})
        },
        u'legion.technology': {
            'Meta': {'object_name': 'Technology'},
            'company': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['legion.Company']", 'through': u"orm['legion.techComp']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'script_alias': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'type_of_tech': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
            'linkedin_code_expires_in': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 8, 7, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'linkedin_secret_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_leads_per_month': ('django.db.models.fields.IntegerField', [], {'default': '500'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Organization']", 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.files.FileField', [], {'default': "'user_photos/no-img.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']"})
        }
    }

    complete_apps = ['legion']