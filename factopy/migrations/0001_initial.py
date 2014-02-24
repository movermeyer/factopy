# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagManager'
        db.create_table(u'factopy_tagmanager', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_string', self.gf('django.db.models.fields.TextField')(default='', db_index=True)),
        ))
        db.send_create_signal('factopy', ['TagManager'])

        # Adding model 'Stream'
        db.create_table(u'factopy_stream', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stream', to=orm['factopy.TagManager'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 22, 0, 0))),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 22, 0, 0))),
        ))
        db.send_create_signal('factopy', ['Stream'])

        # Adding model 'Material'
        db.create_table(u'factopy_material', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_factopy.material_set', null=True, to=orm['contenttypes.ContentType'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('factopy', ['Material'])

        # Adding model 'MaterialStatus'
        db.create_table(u'factopy_materialstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('material', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stream', to=orm['factopy.Material'])),
            ('stream', self.gf('django.db.models.fields.related.ForeignKey')(related_name='materials', to=orm['factopy.Stream'])),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('factopy', ['MaterialStatus'])

        # Adding unique constraint on 'MaterialStatus', fields ['material', 'stream']
        db.create_unique(u'factopy_materialstatus', ['material_id', 'stream_id'])

        # Adding model 'Process'
        db.create_table(u'factopy_process', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polymorphic_factopy.process_set', null=True, to=orm['contenttypes.ContentType'])),
            ('name', self.gf('django.db.models.fields.TextField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(db_index=True)),
        ))
        db.send_create_signal('factopy', ['Process'])

        # Adding model 'ComplexProcess'
        db.create_table(u'factopy_complexprocess', (
            (u'process_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['factopy.Process'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('factopy', ['ComplexProcess'])

        # Adding model 'ProcessOrder'
        db.create_table(u'factopy_processorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('process', self.gf('django.db.models.fields.related.ForeignKey')(related_name='used_by', to=orm['factopy.Process'])),
            ('complex_process', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['factopy.ComplexProcess'])),
        ))
        db.send_create_signal('factopy', ['ProcessOrder'])

        # Adding model 'Adapt'
        db.create_table(u'factopy_adapt', (
            (u'process_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['factopy.Process'], unique=True, primary_key=True)),
            ('stream', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['factopy.Stream'], null=True)),
        ))
        db.send_create_signal('factopy', ['Adapt'])

        # Adding model 'Importer'
        db.create_table(u'factopy_importer', (
            (u'adapt_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['factopy.Adapt'], unique=True, primary_key=True)),
            ('frequency', self.gf('django.db.models.fields.IntegerField')(default=900)),
        ))
        db.send_create_signal('factopy', ['Importer'])

        # Adding model 'Collect'
        db.create_table(u'factopy_collect', (
            (u'process_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['factopy.Process'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('factopy', ['Collect'])

        # Adding model 'Filter'
        db.create_table(u'factopy_filter', (
            (u'process_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['factopy.Process'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('factopy', ['Filter'])


    def backwards(self, orm):
        # Removing unique constraint on 'MaterialStatus', fields ['material', 'stream']
        db.delete_unique(u'factopy_materialstatus', ['material_id', 'stream_id'])

        # Deleting model 'TagManager'
        db.delete_table(u'factopy_tagmanager')

        # Deleting model 'Stream'
        db.delete_table(u'factopy_stream')

        # Deleting model 'Material'
        db.delete_table(u'factopy_material')

        # Deleting model 'MaterialStatus'
        db.delete_table(u'factopy_materialstatus')

        # Deleting model 'Process'
        db.delete_table(u'factopy_process')

        # Deleting model 'ComplexProcess'
        db.delete_table(u'factopy_complexprocess')

        # Deleting model 'ProcessOrder'
        db.delete_table(u'factopy_processorder')

        # Deleting model 'Adapt'
        db.delete_table(u'factopy_adapt')

        # Deleting model 'Importer'
        db.delete_table(u'factopy_importer')

        # Deleting model 'Collect'
        db.delete_table(u'factopy_collect')

        # Deleting model 'Filter'
        db.delete_table(u'factopy_filter')


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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 22, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 22, 0, 0)'}),
            'tags': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stream'", 'to': "orm['factopy.TagManager']"})
        },
        'factopy.tagmanager': {
            'Meta': {'object_name': 'TagManager'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_string': ('django.db.models.fields.TextField', [], {'default': "''", 'db_index': 'True'})
        }
    }

    complete_apps = ['factopy']