# -*- coding: utf-8 -*-
from factopy.models import Stream, Material, MaterialStatus, Filter
from django.test import TestCase
import aspects


class TestFilters(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.filter = Filter.objects.create(name='abstract one')
        self.other_filter = Filter.objects.create(name='abstract two')
        self.other_filter.should_be_cloned = lambda material_status: True
        self.stream = Stream()
        self.stream.save()
        self.materials = [Material() for i in range(5)]
        for i in range(len(self.materials)):
            self.materials[i].save()
            ms = MaterialStatus.objects.get_or_create(
                material=self.materials[i],
                stream=self.stream
            )[0]
            ms.save()

    def test_should_be_cloned(self):
        # check if return false by default.
        for ms in self.stream.materials.all():
            self.assertEquals(self.filter.should_be_cloned(ms), False)
            self.assertEquals(self.other_filter.should_be_cloned(ms), True)

    def test_do(self):
        # check if all the material statuses of the stream are unprocessed.
        processed = MaterialStatus.statuses_name()[u'processed']
        self.assertEquals(
            self.stream.materials.filter(state=processed).count(),
            0)
        # check if it call to should_be_cloned for each material_status of the
        # stream.
        self.materials = []

        def filter_wrap(*args):
            yield aspects.proceed(*args)
            self.materials.append(args[1].material)
            # force the cloning of all the materials
            yield aspects.return_stop(True)
        filters = [self.filter.should_be_cloned]
        aspects.with_wrap(filter_wrap, *filters)
        self.filter.do(self.stream)
        self.assertTrue(len(self.materials) > 0)
        # check if the filtered materials are contained in the input stream.
        for ms in self.stream.materials.all():
            self.assertTrue(ms.material in self.materials)
            self.materials.remove(ms.material)
        self.assertEquals(len(self.materials), 0)
