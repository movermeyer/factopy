# -*- coding: utf-8 -*- 
from factopy.models import *
from django.test import TestCase
import multiprocessing as mp


class TestMachines(TestCase):
    fixtures = [ 'initial_data.yaml', '*']

    def setUp(self):
        self.machine = Machine()
        self.machine.save()
        for i in range(2):
            w = Worker()
            w.machine=self.machine
            w.save()

    def tearDown(self):
        for p in mp.active_children():
            p.terminate()

    def test_bootup(self):
        # check if all the workers are off.
        for w in self.machine.worker_set.all():
            self.assertEquals(w.status(), u'off')
        self.assertEquals(self.machine.status(), u'off')
        # bootup the machine and its workers.
        self.machine.bootup()
        # check if the machine and its workers are running.
        self.assertEquals(self.machine.status(), u'running')
        for w in self.machine.worker_set.all():
            self.assertEquals(w.status(), u'running')

    def test_bootdown(self):
        # check if all the workers are off.
        # bootup the machine and its workers.
        self.machine.bootup()
        # check if the machine and its workers are running.
        self.assertEquals(self.machine.status(), u'running')
        for w in self.machine.worker_set.all():
            self.assertEquals(w.status(), u'running')
        # bootdown the machine and its workers.
        self.machine.bootdown()
        for w in self.machine.worker_set.all():
            self.assertEquals(w.status(), u'off')
        self.assertEquals(self.machine.status(), u'off')