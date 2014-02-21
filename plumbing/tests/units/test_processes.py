# -*- coding: utf-8 -*- 
from plumbing.models import *
from django.test import TestCase
from datetime import datetime
import pytz


class TestProcesses(TestCase):
	fixtures = [ 'initial_data.yaml', '*']

	def setUp(self):
		self.process = Process.objects.get(name='year.Mmonth')
		self.other_process = Process.objects.get(pk=6)
		self.last_process = Process(name='Testing', description='This is a fake process only for testing.')
		self.stream = Stream(root_path="/var/service/data/GVAR_IMG/argentina/")

	def test_serialization(self):
		# check if the __str__ method is defined to return the class name with the name parameter.
		process = u'CollectTimed [year.Mmonth]'
		other_process = u"FilterSolarElevation [Filter night's images]"
		self.assertEquals(str(self.process), str(process))
		self.assertEquals(str(self.other_process), str(other_process))
		# check if the __unicode__ method is defined to return the class name with the name parameter.
		self.assertEquals(unicode(self.process), process)
		self.assertEquals(unicode(self.other_process), other_process)

	def test_mark_with_tags(self):
		# check if the mark_with_tags method in the Process class don't
		# append a new tag into the stream.
		self.process.mark_with_tags(self.stream)
		self.assertTrue(self.stream.empty())
		self.other_process.mark_with_tags(self.stream)
		self.last_process.mark_with_tags(self.stream)
		self.assertTrue(self.stream.empty())