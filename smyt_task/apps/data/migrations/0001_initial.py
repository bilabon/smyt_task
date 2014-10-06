# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'data_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paycheck', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'data', ['User'])

        # Adding model 'Room'
        db.create_table(u'data_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('spots', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'data', ['Room'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'data_user')

        # Deleting model 'Room'
        db.delete_table(u'data_room')


    models = {
        u'data.room': {
            'Meta': {'object_name': 'Room'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {})
        },
        u'data.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['data']