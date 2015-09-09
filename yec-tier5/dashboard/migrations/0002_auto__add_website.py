# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Website'
        db.create_table(u'dashboard_website', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type_of_website', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.User'], null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 4, 22, 0, 0), null=True, blank=True)),
        ))
        db.send_create_signal(u'dashboard', ['Website'])


    def backwards(self, orm):
        # Deleting model 'Website'
        db.delete_table(u'dashboard_website')


    models = {
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
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 22, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'type_of_website': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dashboard']