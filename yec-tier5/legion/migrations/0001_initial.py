# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Industry'
        db.create_table(u'legion_industry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'legion', ['Industry'])

        # Adding model 'User'
        db.create_table(u'legion_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('max_leads_per_month', self.gf('django.db.models.fields.IntegerField')(default=600)),
        ))
        db.send_create_signal(u'legion', ['User'])

        # Adding model 'Person'
        db.create_table(u'legion_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('personal_crunchbase', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('personal_linkedin', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('personal_angellist', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('personal_facebook', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('personal_twitter', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('personal_home_page', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('personal_wikipedia', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('photo', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('times_analyzed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_analyzed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_analyzed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('saved_photo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'legion', ['Person'])

        # Adding M2M table for field interests on 'Person'
        m2m_table_name = db.shorten_name(u'legion_person_interests')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'legion.person'], null=False)),
            ('industry', models.ForeignKey(orm[u'legion.industry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'industry_id'])

        # Adding model 'Job'
        db.create_table(u'legion_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Person'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Company'])),
            ('date_started', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_ended', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=3000)),
        ))
        db.send_create_signal(u'legion', ['Job'])

        # Adding model 'Company'
        db.create_table(u'legion_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('company_crunchbase', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('company_linkedin', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('email_pattern', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('company_angellist', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('company_facebook', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('company_twitter', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('company_wikipedia', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('company_home_page', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('date_founded', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_aquired', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('email_host', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('funding', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('revenue', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('times_analyzed', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('last_analyzed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('number_of_employees', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=3000, blank=True)),
        ))
        db.send_create_signal(u'legion', ['Company'])

        # Adding M2M table for field industries on 'Company'
        m2m_table_name = db.shorten_name(u'legion_company_industries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('company', models.ForeignKey(orm[u'legion.company'], null=False)),
            ('industry', models.ForeignKey(orm[u'legion.industry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['company_id', 'industry_id'])

        # Adding model 'Lead'
        db.create_table(u'legion_lead', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Person'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.User'])),
            ('date_matched', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=3000)),
            ('imported', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('discovered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Document'], null=True, blank=True)),
        ))
        db.send_create_signal(u'legion', ['Lead'])

        # Adding model 'Query'
        db.create_table(u'legion_query', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.User'])),
            ('date_made', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=3000)),
        ))
        db.send_create_signal(u'legion', ['Query'])

        # Adding model 'File'
        db.create_table(u'legion_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=3000)),
        ))
        db.send_create_signal(u'legion', ['File'])

        # Adding model 'Document'
        db.create_table(u'legion_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('date_uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=3000)),
            ('belongs_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.User'], null=True, blank=True)),
            ('is_analyzed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('leads_on_list', self.gf('django.db.models.fields.IntegerField')()),
            ('leads_analyzed', self.gf('django.db.models.fields.IntegerField')()),
            ('exported', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'legion', ['Document'])

        # Adding model 'Snapshot'
        db.create_table(u'legion_snapshot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Person'])),
            ('top_reach', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('avg_reach', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('followed_by', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('following', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('inv_reach', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('closet_contacts', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('influence', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('type_of_person', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('analysis', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('interests', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('news_mentions', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
        ))
        db.send_create_signal(u'legion', ['Snapshot'])


    def backwards(self, orm):
        # Deleting model 'Industry'
        db.delete_table(u'legion_industry')

        # Deleting model 'User'
        db.delete_table(u'legion_user')

        # Deleting model 'Person'
        db.delete_table(u'legion_person')

        # Removing M2M table for field interests on 'Person'
        db.delete_table(db.shorten_name(u'legion_person_interests'))

        # Deleting model 'Job'
        db.delete_table(u'legion_job')

        # Deleting model 'Company'
        db.delete_table(u'legion_company')

        # Removing M2M table for field industries on 'Company'
        db.delete_table(db.shorten_name(u'legion_company_industries'))

        # Deleting model 'Lead'
        db.delete_table(u'legion_lead')

        # Deleting model 'Query'
        db.delete_table(u'legion_query')

        # Deleting model 'File'
        db.delete_table(u'legion_file')

        # Deleting model 'Document'
        db.delete_table(u'legion_document')

        # Deleting model 'Snapshot'
        db.delete_table(u'legion_snapshot')


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
        u'legion.document': {
            'Meta': {'object_name': 'Document'},
            'belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']", 'null': 'True', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'exported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_analyzed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'leads_analyzed': ('django.db.models.fields.IntegerField', [], {}),
            'leads_on_list': ('django.db.models.fields.IntegerField', [], {})
        },
        u'legion.file': {
            'Meta': {'object_name': 'File'},
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'legion.lead': {
            'Meta': {'object_name': 'Lead'},
            'date_matched': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discovered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Document']", 'null': 'True', 'blank': 'True'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']"})
        },
        u'legion.person': {
            'Meta': {'object_name': 'Person'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'birth_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'personal_home_page': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_linkedin': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_twitter': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'personal_wikipedia': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'saved_photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'times_analyzed': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'legion.query': {
            'Meta': {'object_name': 'Query'},
            'date_made': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.User']"})
        },
        u'legion.snapshot': {
            'Meta': {'object_name': 'Snapshot'},
            'analysis': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'avg_reach': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'closet_contacts': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['legion']