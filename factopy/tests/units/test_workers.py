# -*- coding: utf-8 -*- 
from factopy.models import *
from django.test import TestCase
import threading


class TestWorkers(TestCase):
	fixtures = [ 'initial_data.yaml', '*']

	def setUp(self):
		self.worker = Worker()

	def test_bootup(self):
		# count the amount of threads.
		count = threading.active_count()
		# check if the worker create his own thread.
		self.worker.bootup()
		self.assertEquals(threading.active_count(), count + 1)
		self.worker.bootdown()

	def test_bootdown(self):
		# count the amount of threads when the worker is running.
		self.worker.bootup()
		count = threading.active_count()
		# check if the worker finish his own thread.
		self.worker.bootdown()
		self.assertEquals(threading.active_count(), count - 1)