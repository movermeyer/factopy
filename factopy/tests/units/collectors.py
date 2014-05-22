# -*- coding: utf-8 -*-
from factopy.models import Stream, Material, MaterialStatus, Collect
from django.test import TestCase


class TestCollectors(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.collect = Collect.objects.create(name='abstract one')
        self.other_collect = Collect.objects.create(name='abstract two')
        self.other_collect.get_key = lambda material_status: "even" \
            if material_status.material.id % 2 == 0 else "uneven"
        self.stream = Stream()
        self.stream.save()
        self.materials = [Material() for i in range(1, 13)]
        for i in range(len(self.materials)):
            self.materials[i].save()
            ms = MaterialStatus.objects.get_or_create(
                material=self.materials[i],
                stream=self.stream,
                state=(1 if (i % 2 == 0) else 0)
            )[0]
            ms.save()

    def test_get_key(self):
        # check if the abstract class should raise an exception because these
        # method doesn't exist on an abstract class.
        with self.assertRaises(AttributeError) as err:
            self.collect.get_key(self.stream.materials.all()[0])
        self.assertEquals(
            unicode(err.exception),
            u"'Collect' object has no attribute 'get_key'")

    def test_get_keys(self):
        # check if when this is sended to an abstract class should raise the
        # same exception that with get_key.
        with self.assertRaises(AttributeError) as err:
            self.collect.get_keys(self.stream)
        self.assertEquals(
            unicode(err.exception),
            u"'Collect' object has no attribute 'get_key'")
        # check if when a fake get_key method exists, a set of uniques keys is
        # returned.
        keys = self.other_collect.get_keys(self.stream)
        self.assertEquals(len(keys), 2)
        for key in keys:
            self.assertTrue(key in ["even", "uneven"])

    def test_init_empty_streams(self):
        # check if when this is sended to an abstract class should raise the
        # same exception that with get_key.
        with self.assertRaises(AttributeError) as err:
            self.collect.init_empty_streams(self.stream)
        self.assertEquals(
            unicode(err.exception),
            u"'Collect' object has no attribute 'get_key'")
        # check if when a fake get_key method exists, a set of uniques keys is
        # returned.
        streams = self.other_collect.init_empty_streams(self.stream)
        self.assertEquals(len(streams.keys()), 2)
        for key in streams.keys():
            self.assertTrue(key in ["even", "uneven"])
            self.assertTrue(streams[key].empty())

    def test_step(self):
        # check if all the material statuses of the stream are unprocessed.
        processed = MaterialStatus.statuses_name()[u'processed']
        self.assertEquals(
            self.stream.materials.filter(state=processed).count(),
            0)
        # check if collect materials into two differents streams: even and
        # uneven (with the fake get_key).
        for fs in self.stream.unprocessed():
            self.assertFalse(fs.processed)
