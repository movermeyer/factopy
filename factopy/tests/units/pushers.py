# -*- coding: utf-8 -*-
from factopy.models import Stream, Push
from django.test import TestCase
import threading
from datetime import datetime, timedelta
import pytz


class TestPushs(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.stream = Stream()
        self.stream.save()
        self.pusher = Push.objects.get_or_create(name='abstract one')[0]
        self.now = datetime.utcnow().replace(tzinfo=pytz.UTC)
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

    def test_should_adapt(self):
        # check if should_adapt return false until the right time.
        self.pusher.frequency = 10
        delta = timedelta(seconds=self.pusher.frequency - 1)
        self.pusher.previous = self.now - delta
        self.assertFalse(self.pusher.should_adapt())
        self.assertEquals(self.pusher.previous, self.now - delta)
        # check if should_adapt return true after the right time.
        delta = timedelta(seconds=self.pusher.frequency + 1)
        self.pusher.previous = self.now - delta
        self.assertTrue(self.pusher.should_adapt())
        self.assertNotEquals(self.pusher.previous, self.now - delta)
