# -*- coding: utf-8 -*-
from factopy.models import Filter
from django.test import TestCase


class TestFilters(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.filter = Filter.objects.get_or_create(name='Filter materials')[0]
        self.other_filter = Filter.objects.get_or_create(
            name='Another filter')[0]
        self.other_filter.should_be_cloned = lambda material_status: True
        self.stream = self.other_filter.streams.all()[0]

    def test_should_be_cloned(self):
        # check if return false by default.
        for ms in self.stream.materials.all():
            self.assertEquals(self.filter.should_be_cloned(ms), False)
            self.assertEquals(self.other_filter.should_be_cloned(ms), True)

    def test_step(self):
        # check if it call to should_be_cloned for each unprocessed
        # material_status of the streams.
        self.materials = []
        self.old_method = self.other_filter.should_be_cloned

        def wrap(*args):
            it_should = self.old_method(*args)
            if it_should:
                self.materials.append(args[0].material)
            return it_should
        self.other_filter.should_be_cloned = wrap
        self.other_filter.step()
        self.assertTrue(len(self.materials) > 0)
        # check if the filtered materials are contained in the input stream.
        for ms in self.stream.materials.all():
            self.assertTrue(ms.material in self.materials)
            self.materials.remove(ms.material)
        self.assertEquals(len(self.materials), 0)
