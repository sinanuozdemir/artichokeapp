# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Connection'
        db.create_table(u'dashboard_connection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legion.Person'], null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.User'], null=True, blank=True)),
            ('new', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('following', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('followed_by', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linkedin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebook', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('crunchbase', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('angellist', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'dashboard', ['Connection'])

        # Adding M2M table for field subscribed_to on 'Connection'
        m2m_table_name = db.shorten_name(u'dashboard_connection_subscribed_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('connection', models.ForeignKey(orm[u'dashboard.connection'], null=False)),
            ('website', models.ForeignKey(orm[u'dashboard.website'], null=False))
        ))
        db.create_unique(m2m_table_name, ['connection_id', 'website_id'])


    def backwards(self, orm):
        # Deleting model 'Connection'
        db.delete_table(u'dashboard_connection')

        # Removing M2M table for field subscribed_to on 'Connection'
        db.delete_table(db.shorten_name(u'dashboard_connection_subscribed_to'))


    models = {
        u'dashboard.connection': {
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
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legion.Person']", 'null': 'True', 'blank': 'True'}),
            'subscribed_to': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.Website']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        },
        u'dashboard.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'dashboard.website': {
            'Meta': {'object_name': 'Website'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 23, 0, 0)', 'null': 'True', 'blank': 'True'}),
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
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 23, 0, 0)'}),
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
        }
    }

    complete_apps = ['dashboard']