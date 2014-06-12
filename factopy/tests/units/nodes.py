# -*- coding: utf-8 -*-
from factopy.models import Node, Stream
from django.test import TestCase
import multiprocessing


class TestNodes(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.model = Node.objects.get(pk=1)

    def tearDown(self):
        self.model.change_status(u'off')

    def test_serialization(self):
        # check if the __str__ method is defined to return the class name with
        # the status.
        model = u"Node [status: off]"
        self.assertEquals(str(self.model), str(model))
        # check if the __unicode__ method is defined to return the class name
        # with the status.
        self.assertEquals(unicode(self.model), model)

    def test_bootup(self):
        # check if bootup update the ip and create self.managers
        # multiprocessing Pool.
        old_ip = self.model.ip
        self.assertFalse(hasattr(self.model, 'managers'))
        self.model.bootup()
        self.assertNotEquals(self.model.ip, old_ip)
        self.assertTrue(hasattr(self.model, 'managers'))
        self.assertEquals(self.model.managers.__class__,
                          multiprocessing.pool.Pool)

    def test_step(self):
        # check if the node distribute the unnprocessed streams through
        # the Pool.
        self.model.bootup()
        self.flag = False
        original_map = self.model.managers.map

        def wrap(managers, ids):
            self.flag = True
            l = Stream.requiring_work().values_list('id', flat=True)
            self.assertEquals(len(ids), len(l))
            for i in ids:
                self.assertIn(i, l)
            return original_map(managers, ids)
        self.model.managers.map = wrap
        self.model.step()
        self.assertTrue(self.flag)
        self.model.bootdown()
