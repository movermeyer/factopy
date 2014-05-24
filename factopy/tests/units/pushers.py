# -*- coding: utf-8 -*-
from factopy.models import Stream, Push
from django.test import TestCase
import threading


class TestPushs(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.stream = Stream()
        self.stream.save()
        self.pusher = Push.objects.get_or_create(name='abstract one')[0]
        self.pusher.streams.add(self.stream)

    def test_setup_unloaded(self):
        # check if create a thread for each unloaded pusher.
        self.actives = threading.activeCount()
        self.unloaded = [i for i in Push.objects.all()
                         if not hasattr(i, 'thread')]
        self.loaded = Push.setup_unloaded()
        self.assertEquals(
            self.actives + len(self.unloaded),
            threading.activeCount())
        for i in self.loaded:
            i.thread.cancel()
