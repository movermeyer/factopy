# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagManager'
        db.create_table(u'plumbing_tagmanager', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_string', self.gf('django.db.models.fields.TextField')(default='', db_index=True)),
        ))
        db.send_create_signal('plumbing', ['TagManager'])

        # Adding model 'Stream'
        db.create_table(u'plumbing_stream', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stream', to=orm['plumbing.TagManager'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 22, 0, 0))),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 22, 0, 0))),
        ))
        db.send_create_signal('plumbing', ['Stream'])

        # Adding model 'Material'
        db.create_table(u'plumbing_material', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_plumbing.material_set', null=True, to=orm['contenttypes.ContentType'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('plumbing', ['Material'])

        # Adding model 'MaterialStatus'
        db.create_table(u'plumbing_materialstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('material', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stream', to=orm['plumbing.Material'])),
            ('stream', self.gf('django.db.models.fields.related.ForeignKey')(related_name='materials', to=orm['plumbing.Stream'])),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('plumbing', ['MaterialStatus'])

        # Adding unique constraint on 'MaterialStatus', fields ['material', 'stream']
        db.create_unique(u'plumbing_materialstatus', ['material_id', 'stream_id'])

        # Adding model 'Process'
        db.create_table(u'plumbing_process', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_plumbing.process_set', null=True, to=orm['contenttypes.ContentType'])),
            ('name', self.gf('django.db.models.fields.TextField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(db_index=True)),
        ))
        db.send_create_signal('plumbing', ['Process'])

        # Adding model 'ComplexProcess'
        db.create_table(u'plumbing_complexprocess', (
            (u'process_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['plumbing.Process'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('plumbing', ['ComplexProcess'])

        # Adding model 'ProcessOrder'
        db.create_table(u'plumbing_processorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('process', self.gf('django.db.models.fields.related.ForeignKey')(related_name='used_by', to=orm['plumbing.Process'])),
            ('complex_process', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plumbing.ComplexProcess'])),
        ))
        db.send_create_signal('plumbing', ['ProcessOrder'])

        # Adding model 'Adapt'
        db.create_table(u'plumbing_adapt', (
            (u'process_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['plumbing.Process'], unique=True, primary_key=True)),
            ('stream', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['plumbing.Stream'], null=True)),
        ))
        db.send_create_signal('plumbing', ['Adapt'])

        # Adding model 'Importer'
        db.create_table(u'plumbing_importer', (
            (u'adapt_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['plumbing.Adapt'], unique=True, primary_key=True)),
            ('frequency', self.gf('django.db.models.fields.IntegerField')(default=900)),
        ))
        db.send_create_signal('plumbing', ['Importer'])

        # Adding model 'Collect'
        db.create_table(u'plumbing_collect', (
            (u'process_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['plumbing.Process'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('plumbing', ['Collect'])

        # Adding model 'Filter'
        db.create_table(u'plumbing_filter', (
            (u'process_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['plumbing.Process'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('plumbing', ['Filter'])


    def backwards(self, orm):
        # Removing unique constraint on 'MaterialStatus', fields ['material', 'stream']
        db.delete_unique(u'plumbing_materialstatus', ['material_id', 'stream_id'])

        # Deleting model 'TagManager'
        db.delete_table(u'plumbing_tagmanager')

        # Deleting model 'Stream'
        db.delete_table(u'plumbing_stream')

        # Deleting model 'Material'
        db.delete_table(u'plumbing_material')

        # Deleting model 'MaterialStatus'
        db.delete_table(u'plumbing_materialstatus')

        # Deleting model 'Process'
        db.delete_table(u'plumbing_process')

        # Deleting model 'ComplexProcess'
        db.delete_table(u'plumbing_complexprocess')

        # Deleting model 'ProcessOrder'
        db.delete_table(u'plumbing_processorder')

        # Deleting model 'Adapt'
        db.delete_table(u'plumbing_adapt')

        # Deleting model 'Importer'
        db.delete_table(u'plumbing_importer')

        # Deleting model 'Collect'
        db.delete_table(u'plumbing_collect')

        # Deleting model 'Filter'
        db.delete_table(u'plumbing_filter')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'plumbing.adapt': {
            'Meta': {'object_name': 'Adapt', '_ormbases': ['plumbing.Process']},
            u'process_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['plumbing.Process']", 'unique': 'True', 'primary_key': 'True'}),
            'stream': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['plumbing.Stream']", 'null': 'True'})
        },
        'plumbing.collect': {
            'Meta': {'object_name': 'Collect', '_ormbases': ['plumbing.Process']},
            u'process_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['plumbing.Process']", 'unique': 'True', 'primary_key': 'True'})
        },
        'plumbing.complexprocess': {
            'Meta': {'object_name': 'ComplexProcess', '_ormbases': ['plumbing.Process']},
            u'process_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['plumbing.Process']", 'unique': 'True', 'primary_key': 'True'}),
            'processes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'complex_process'", 'symmetrical': 'False', 'through': "orm['plumbing.ProcessOrder']", 'to': "orm['plumbing.Process']"})
        },
        'plumbing.filter': {
            'Meta': {'object_name': 'Filter', '_ormbases': ['plumbing.Process']},
            u'process_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['plumbing.Process']", 'unique': 'True', 'primary_key': 'True'})
        },
        'plumbing.importer': {
            'Meta': {'object_name': 'Importer', '_ormbases': ['plumbing.Adapt']},
            u'adapt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['plumbing.Adapt']", 'unique': 'True', 'primary_key': 'True'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'default': '900'})
        },
        'plumbing.material': {
            'Meta': {'object_name': 'Material'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_plumbing.material_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"})
        },
        'plumbing.materialstatus': {
            'Meta': {'unique_together': "(('material', 'stream'),)", 'object_name': 'MaterialStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stream'", 'to': "orm['plumbing.Material']"}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stream': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'materials'", 'to': "orm['plumbing.Stream']"})
        },
        'plumbing.process': {
            'Meta': {'object_name': 'Process'},
            'description': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_plumbing.process_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"})
        },
        'plumbing.processorder': {
            'Meta': {'object_name': 'ProcessOrder'},
            'complex_process': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['plumbing.ComplexProcess']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'process': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'used_by'", 'to': "orm['plumbing.Process']"})
        },
        'plumbing.stream': {
            'Meta': {'object_name': 'Stream'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 22, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 22, 0, 0)'}),
            'tags': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stream'", 'to': "orm['plumbing.TagManager']"})
        },
        'plumbing.tagmanager': {
            'Meta': {'object_name': 'TagManager'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_string': ('django.db.models.fields.TextField', [], {'default': "''", 'db_index': 'True'})
        }
    }

    complete_apps = ['plumbing']