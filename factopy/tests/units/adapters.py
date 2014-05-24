# -*- coding: utf-8 -*-
from factopy.models import Stream, Adapt
from django.test import TestCase


class TestAdapters(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.stream = Stream()
        self.stream.save()
        self.adapter = Adapt.objects.get_or_create(name='abstract one')[0]
        self.adapter.streams.add(self.stream)

    def test_update(self):
        # check if the update method raise a "Subclass responsability"
        # exception  because the subclass should implement the method update.
        with self.assertRaises(Exception) as err:
            self.adapter.update()
        self.assertEquals(unicode(err.exception), u"Subclass responsability")

    def test_should_adapt(self):
        # by default an adapter should not adapt anything.
        self.assertFalse(self.adapter.should_adapt())

    def test_step(self):
        # by default dont should execute the update.
        self.assertEquals(self.adapter.step(), None)
        # when a subclass should_adapt, it execute the update and raise
        # the exception.
        self.adapter.should_adapt = lambda: True
        with self.assertRaises(Exception) as err:
            self.adapter.step()
        self.assertEquals(unicode(err.exception), u"Subclass responsability")
