# -*- coding: utf-8 -*-
from factopy.models import Stream, Material, MaterialStatus
from django.test import TestCase
from datetime import datetime
import pytz


class TestStreams(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.begin = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.stream = Stream.objects.get_or_create(id=6)[0]
        self.other_stream = Stream()
        self.other_stream.save()
        self.end = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.materials = self.stream.materials.all()[:]
        for i in range(len(self.materials)):
            state = 0 if (i % 2 == 0) else 2
            self.materials[i].state = state
            self.materials[i].save()

    def test_serialization(self):
        # check if the __str__ method is defined to return the object pk and
        # parameter.
        result = u'[id: %s unprocessed: %s] -> %s' % (
            unicode(self.stream.pk),
            unicode(self.stream.unprocessed_count),
            unicode(self.stream.feed)
        )
        self.assertEquals(str(self.stream), str(result))
        # check if the __unicode__ method is defined to return the object pk
        # parameter.
        self.assertEquals(unicode(self.stream), result)

    def test_save(self):
        # check if hte instance was created between the begining and the ending
        # of the setup.
        self.assertTrue(self.begin <= self.other_stream.created <= self.end)
        # check if the created and modified datetime are equals
        self.assertEquals(self.other_stream.created, self.other_stream.modified)
        # check if the modified datetime change when the objects is saved
        # again.
        self.other_stream.save()
        self.assertTrue(self.other_stream.modified > self.other_stream.created)

    def test_clone(self):
        # check if the clone method create a new stream.
        clone = self.stream.clone()
        self.assertNotEquals(clone, self.stream)
        # check if the cloned stream is different from the original
        self.assertNotEquals(clone, self.stream)
        # self.assertEquals(clone, self.stream)
        # check if the cloned stream is empty, and if the clone method avoid
        # clone the files.
        self.assertEquals(self.stream.materials.count(), 5)
        self.assertEquals(clone.materials.count(), 0)

    def test_unprocessed(self):
        # check if return only the unprocessed files.
        for fs in self.stream.unprocessed():
            self.assertFalse(fs.processed)
            fs.delete()
        # check if return an empty list when it don't have pending files.
        self.assertEquals(self.stream.unprocessed().count(), 0)

    def test_empty(self):
        # check if return True when it has got pending files.
        self.assertFalse(self.stream.empty())
        for fs in self.stream.unprocessed():
            fs.delete()
        # check if return False when it hasn't got pending files.
        self.assertTrue(self.stream.empty())

    def test_create_empty(self):
        # check if it create an empty stream.
        stream = Stream.create_empty()
        self.assertEquals(stream.__class__, Stream)
        self.assertEquals(stream.unprocessed_count, 0)
        self.assertEquals(stream.feed, None)
        self.assertEquals(Stream.objects.filter(id=stream.id).count(), 1)

    def test_requiring_work(self):
        # check if return all the streams with pending material statusese.
        self.assertEquals(len(Stream.requiring_work()), 1)
        self.assertEquals(Stream.requiring_work()[0], self.stream)
        [ms.clone_for(self.other_stream) for ms in self.stream.materials.all()]
        self.assertEquals(len(Stream.requiring_work()), 2)
        self.assertEquals(Stream.requiring_work()[0], self.stream)
