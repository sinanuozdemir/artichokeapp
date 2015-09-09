# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Document'
        db.delete_table(u'legion_document')

        # Deleting model 'Website'
        db.delete_table(u'legion_website')

        # Deleting model 'File'
        db.delete_table(u'legion_file')

        # Deleting model 'Snapshot'
        db.delete_table(u'legion_snapshot')

        # Deleting model 'NewsArticle'
        db.delete_table(u'legion_newsarticle')

        # Deleting field 'Lead.document'
        db.delete_column(u'legion_lead', 'document_id')

        # Removing M2M table for field source on 'EmailAddress'
        db.delete_table(db.shorten_name(u'legion_emailaddress_source'))


    def backwards(self, orm):
        # Adding model 'Document'
        db.create_table(u'legion_document', (
            ('belongs_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.User'], null=True, blank=True)),
            ('exported', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('leads_on_list', self.gf('django.db.models.fields.IntegerField')()),
            ('leads_analyzed', self.gf('django.db.models.fields.IntegerField')()),
            ('is_analyzed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_uploaded', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 4, 29, 0, 0))),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'legion', ['Document'])

        # Adding model 'Website'
        db.create_table(u'legion_website', (
            ('blog', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Person'], null=True, blank=True)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('social_media', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 4, 29, 0, 0), null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Company'], null=True, blank=True)),
            ('type_of_media', self.gf('django.db.models.fields.CharField')(max_length=25)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'legion', ['Website'])

        # Adding model 'File'
        db.create_table(u'legion_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_uploaded', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 4, 29, 0, 0))),
        ))
        db.send_create_signal(u'legion', ['File'])

        # Adding model 'Snapshot'
        db.create_table(u'legion_snapshot', (
            ('interests', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('avg_reach', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('inv_reach', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('closet_contacts', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('followed_by', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('influence', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('analysis', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Person'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 4, 29, 0, 0))),
            ('type_of_person', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('following', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('news_mentions', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('top_reach', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'legion', ['Snapshot'])

        # Adding model 'NewsArticle'
        db.create_table(u'legion_newsarticle', (
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Person'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('date_written', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'legion', ['NewsArticle'])

        # Adding field 'Lead.document'
        db.add_column(u'legion_lead', 'document',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Document'], null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field source on 'EmailAddress'
        m2m_table_name = db.shorten_name(u'legion_emailaddress_source')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('emailaddress', models.ForeignKey(orm[u'legion.emailaddress'], null=False)),
            ('website', models.ForeignKey(orm[u'legion.website'], null=False))
        ))
        db.create_unique(m2m_table_name, ['emailaddress_id', 'website_id'])


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
            'address': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deliverable': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 3, 0, 0)', 'null': 'True', 'blank': 'True'}),
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
            'date_matched': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 3, 0, 0)'}),
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
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 3, 0, 0)'}),
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
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 3, 0, 0)'}),
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
        },
        u'legion.query': {
            'Meta': {'ordering': "['-date_made']", 'object_name': 'Query'},
            'date_made': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 3, 0, 0)'}),
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
            'linkedin_code_expires_in': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 3, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'linkedin_secret_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_leads_per_month': ('django.db.models.fields.IntegerField', [], {'default': '500'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Organization']", 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.files.FileField', [], {'default': "'user_photos/no-img.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']"})
        }
    }

    complete_apps = ['legion']