# -*- coding: utf-8 -*- 
from factopy.models import *
from django.test import TestCase
import multiprocessing as mp
import threading


class TestWorkers(TestCase):
	fixtures = [ 'initial_data.yaml', '*']

	def setUp(self):
		self.worker = Worker()

	def tearDown(self):
		for p in mp.active_children():
			p.terminate()

	def test_bootup(self):
		# check if the worker create his own thread.
		self.assertEquals(self.worker.status(), u'off')
		self.worker.bootup()
		self.assertIn(self.worker, mp.active_children())
		self.assertEquals(self.worker.status(), u'running')
		# finish the thread.
		self.worker.bootdown()
		self.assertEquals(self.worker.status(), u'off')


	def test_bootdown(self):
		# count the amount of threads when the worker is running.
		self.assertEquals(self.worker.status(), u'off')
		self.worker.bootup()
		self.assertEquals(self.worker.status(), u'running')
		# check if the worker finish his own thread.
		self.worker.bootdown()
		self.assertEquals(self.worker.status(), u'off')
		self.worker.terminate()
		# TODO: Make the next assert work
		#self.assertNotIn(self.worker, mp.active_children())