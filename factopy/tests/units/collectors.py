# -*- coding: utf-8 -*- 
from factopy.models import *
from django.test import TestCase
from datetime import datetime
import pytz
import random


class TestCollectors(TestCase):
	fixtures = [ 'initial_data.yaml', '*']

	def setUp(self):
		self.collect = Collect.objects.create(name='abstract one')
		self.other_collect = Collect.objects.create(name='abstract two')
		self.other_collect.get_key = lambda material_status: "even" if material_status.material.id % 2 == 0 else "uneven"
		self.stream = Stream()
		self.stream.save()
		self.materials = [ Material() for i in range(1,13) ]
		for i in range(len(self.materials)):
			self.materials[i].save()
			ms = MaterialStatus.objects.get_or_create(material=self.materials[i],stream=self.stream,processed=(i%2==0))[0]
			ms.save()

	def test_mark_with_tags(self):
		# check if the mark_with_tags method in the Collect class don't
		# append a new tag into the stream.
		self.assertTrue(self.stream.tags.empty())
		self.collect.mark_with_tags(self.stream)
		self.assertTrue(self.stream.tags.empty())

	def test_get_key(self):
		# check if the abstract class should raise an exception because these method doesn't
		# exist on an abstract class.
		with self.assertRaises(AttributeError) as err:
			self.collect.get_key(self.stream.materials.all()[0])
		self.assertEquals(unicode(err.exception), u"'Collect' object has no attribute 'get_key'")

	def test_get_keys(self):
		# check if when this is sended to an abstract class should raise the same exception that
		# with get_key.
		with self.assertRaises(AttributeError) as err:
			self.collect.get_keys(self.stream)
		self.assertEquals(unicode(err.exception), u"'Collect' object has no attribute 'get_key'")
		# check if when a fake get_key method exists, a set of uniques keys is returned.
		keys = self.other_collect.get_keys(self.stream)
		self.assertEquals(len(keys), 2)
		for key in keys:
			self.assertTrue(key in ["even", "uneven"])

	def test_init_empty_streams(self):
		# check if when this is sended to an abstract class should raise the same exception that
		# with get_key.
		with self.assertRaises(AttributeError) as err:
			self.collect.init_empty_streams(self.stream)
		self.assertEquals(unicode(err.exception), u"'Collect' object has no attribute 'get_key'")
		# check if when a fake get_key method exists, a set of uniques keys is returned.
		streams = self.other_collect.init_empty_streams(self.stream)
		self.assertEquals(len(streams.keys()), 2)
		for key in streams.keys():
			self.assertTrue(key in ["even", "uneven"])
			self.assertTrue(streams[key].empty())

	def test_do(self):
		# check if all the material statuses of the stream are unprocessed.
		self.assertTrue(self.stream.materials.filter(processed=True).count(), 0)
		# check if collect materials into two differents streams: even and uneven (with the fake
		# get_key).
		other = {"even": "uneven", "uneven": "even"}
		result = self.other_collect.do(self.stream)
		for fs in self.stream.materials.all():
			self.assertTrue(fs.processed)
			key = self.other_collect.get_key(fs)
			stream = [s for s in result if s.tags.exist(key)][0]
			other_stream = [s for s in result if s.tags.exist(other[key])][0]
			self.assertNotEquals(stream, [])
			self.assertTrue(fs.material in [ f.material for f in stream.materials.all()])
			self.assertFalse(fs.material in [ f.material for f in other_stream.materials.all()])