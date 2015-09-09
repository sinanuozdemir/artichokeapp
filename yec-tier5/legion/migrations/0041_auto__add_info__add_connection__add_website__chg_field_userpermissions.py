# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Info'
        db.create_table(u'legion_info', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type_of_info', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('person_belongs_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Person'], null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 3, 20, 0, 0), null=True, blank=True)),
            ('information', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('company_belongs_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Company'], null=True, blank=True)),
            ('is_current', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'legion', ['Info'])

        # Adding M2M table for field source on 'Info'
        m2m_table_name = db.shorten_name(u'legion_info_source')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('info', models.ForeignKey(orm[u'legion.info'], null=False)),
            ('website', models.ForeignKey(orm[u'legion.website'], null=False))
        ))
        db.create_unique(m2m_table_name, ['info_id', 'website_id'])

        # Adding model 'Connection'
        db.create_table(u'legion_connection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Person'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.User'], null=True, blank=True)),
            ('new', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Organization'], null=True, blank=True)),
            ('lead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('following', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('followed_by', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linkedin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebook', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('crunchbase', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('angellist', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('subscribed_to', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'legion', ['Connection'])

        # Adding model 'Website'
        db.create_table(u'legion_website', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type_of_media', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('social_media', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('blog', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('person_belongs_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Person'], null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 3, 20, 0, 0), null=True, blank=True)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('company_belongs_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Company'], null=True, blank=True)),
        ))
        db.send_create_signal(u'legion', ['Website'])


        # Changing field 'UserPermissions.profile_picture'
        db.alter_column(u'legion_userpermissions', 'profile_picture', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))

    def backwards(self, orm):
        # Deleting model 'Info'
        db.delete_table(u'legion_info')

        # Removing M2M table for field source on 'Info'
        db.delete_table(db.shorten_name(u'legion_info_source'))

        # Deleting model 'Connection'
        db.delete_table(u'legion_connection')

        # Deleting model 'Website'
        db.delete_table(u'legion_website')


        # Changing field 'UserPermissions.profile_picture'
        db.alter_column(u'legion_userpermissions', 'profile_picture', self.gf('django.db.models.fields.files.FileField')(max_length=100))

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
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000', 'blank': 'True'}),
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
        u'legion.connection': {
            'Meta': {'object_name': 'Connection'},
            'angellist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'crunchbase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'followed_by': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'following': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'linkedin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Organization']", 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'subscribed_to': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']", 'null': 'True', 'blank': 'True'})
        },
        u'legion.document': {
            'Meta': {'object_name': 'Document'},
            'belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']", 'null': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 20, 0, 0)'}),
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'exported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_analyzed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'leads_analyzed': ('django.db.models.fields.IntegerField', [], {}),
            'leads_on_list': ('django.db.models.fields.IntegerField', [], {})
        },
        u'legion.education': {
            'Meta': {'object_name': 'Education'},
            'date_ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'education_level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            'fields_of_study': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['legion.Industry']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']"}),
            'school_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'legion.file': {
            'Meta': {'object_name': 'File'},
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 20, 0, 0)'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'legion.industry': {
            'Meta': {'object_name': 'Industry'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'legion.info': {
            'Meta': {'object_name': 'Info'},
            'company_belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 20, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'person_belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['legion.Website']", 'null': 'True', 'blank': 'True'}),
            'type_of_info': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'legion.job': {
            'Meta': {'object_name': 'Job'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']"}),
            'date_ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'months': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'legion.lead': {
            'Meta': {'object_name': 'Lead'},
            'date_matched': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 20, 0, 0)'}),
            'discovered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Document']", 'null': 'True', 'blank': 'True'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
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
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 20, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Lead']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '10000', 'null': 'True'})
        },
        u'legion.newsarticle': {
            'Meta': {'object_name': 'NewsArticle'},
            'date_written': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'legion.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_of_organization': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'legion.person': {
            'Meta': {'object_name': 'Person'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'birth_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 20, 0, 0)'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['legion.Industry']", 'symmetrical': 'False'}),
            'is_analyzed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_analyzed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_angellist': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_crunchbase': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_facebook': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_github': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'personal_home_page': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_linkedin': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_twitter': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_wikipedia': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'saved_photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'times_analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'legion.query': {
            'Meta': {'ordering': "['-date_made']", 'object_name': 'Query'},
            'date_made': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 20, 0, 0)'}),
            'email_counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'emails_produced': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
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
        u'legion.snapshot': {
            'Meta': {'object_name': 'Snapshot'},
            'analysis': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'avg_reach': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'closet_contacts': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 20, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'followed_by': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'following': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'influence': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'interests': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'inv_reach': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'news_mentions': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']"}),
            'top_reach': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'type_of_person': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'})
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
            'linkedin_code_expires_in': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 20, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'linkedin_secret_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_leads_per_month': ('django.db.models.fields.IntegerField', [], {'default': '500'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Organization']", 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.files.FileField', [], {'default': "'user_photos/no-img.jpg'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']"})
        },
        u'legion.website': {
            'Meta': {'object_name': 'Website'},
            'blog': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company_belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Company']", 'null': 'True', 'blank': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 20, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'person_belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'social_media': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type_of_media': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['legion']