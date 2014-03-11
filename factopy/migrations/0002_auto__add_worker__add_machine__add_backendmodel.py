# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Worker'
        db.create_table(u'factopy_worker', (
            (u'backendmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['factopy.BackendModel'], unique=True, primary_key=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factopy.Machine'])),
        ))
        db.send_create_signal('factopy', ['Worker'])

        # Adding model 'Machine'
        db.create_table(u'factopy_machine', (
            (u'backendmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['factopy.BackendModel'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('factopy', ['Machine'])

        # Adding model 'BackendModel'
        db.create_table(u'factopy_backendmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_factopy.backendmodel_set', null=True, to=orm['contenttypes.ContentType'])),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('factopy', ['BackendModel'])


    def backwards(self, orm):
        # Deleting model 'Worker'
        db.delete_table(u'factopy_worker')

        # Deleting model 'Machine'
        db.delete_table(u'factopy_machine')

        # Deleting model 'BackendModel'
        db.delete_table(u'factopy_backendmodel')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'factopy.adapt': {
            'Meta': {'object_name': 'Adapt', '_ormbases': ['factopy.Process']},
            u'process_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['factopy.Process']", 'unique': 'True', 'primary_key': 'True'}),
            'stream': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['factopy.Stream']", 'null': 'True'})
        },
        'factopy.backendmodel': {
            'Meta': {'object_name': 'BackendModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_factopy.backendmodel_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'factopy.collect': {
            'Meta': {'object_name': 'Collect', '_ormbases': ['factopy.Process']},
            u'process_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['factopy.Process']", 'unique': 'True', 'primary_key': 'True'})
        },
        'factopy.complexprocess': {
            'Meta': {'object_name': 'ComplexProcess', '_ormbases': ['factopy.Process']},
            u'process_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['factopy.Process']", 'unique': 'True', 'primary_key': 'True'}),
            'processes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'complex_process'", 'symmetrical': 'False', 'through': "orm['factopy.ProcessOrder']", 'to': "orm['factopy.Process']"})
        },
        'factopy.filter': {
            'Meta': {'object_name': 'Filter', '_ormbases': ['factopy.Process']},
            u'process_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['factopy.Process']", 'unique': 'True', 'primary_key': 'True'})
        },
        'factopy.importer': {
            'Meta': {'object_name': 'Importer', '_ormbases': ['factopy.Adapt']},
            u'adapt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['factopy.Adapt']", 'unique': 'True', 'primary_key': 'True'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'default': '900'})
        },
        'factopy.machine': {
            'Meta': {'object_name': 'Machine', '_ormbases': ['factopy.BackendModel']},
            u'backendmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['factopy.BackendModel']", 'unique': 'True', 'primary_key': 'True'})
        },
        'factopy.material': {
            'Meta': {'object_name': 'Material'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_factopy.material_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"})
        },
        'factopy.materialstatus': {
            'Meta': {'unique_together': "(('material', 'stream'),)", 'object_name': 'MaterialStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stream'", 'to': "orm['factopy.Material']"}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stream': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'materials'", 'to': "orm['factopy.Stream']"})
        },
        'factopy.process': {
            'Meta': {'object_name': 'Process'},
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_factopy.process_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"})
        },
        'factopy.processorder': {
            'Meta': {'object_name': 'ProcessOrder'},
            'complex_process': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['factopy.ComplexProcess']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'process': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'used_by'", 'to': "orm['factopy.Process']"})
        },
        'factopy.stream': {
            'Meta': {'object_name': 'Stream'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 10, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 10, 0, 0)'}),
            'tags': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stream'", 'to': "orm['factopy.TagManager']"})
        },
        'factopy.tagmanager': {
            'Meta': {'object_name': 'TagManager'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_string': ('django.db.models.fields.TextField', [], {'default': "''", 'db_index': 'True'})
        },
        'factopy.worker': {
            'Meta': {'object_name': 'Worker', '_ormbases': ['factopy.BackendModel']},
            u'backendmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['factopy.BackendModel']", 'unique': 'True', 'primary_key': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['factopy.Machine']"})
        }
    }

    complete_apps = ['factopy']