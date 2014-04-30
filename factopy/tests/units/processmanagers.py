# -*- coding: utf-8 -*-
from factopy.models import Process
from django.test import TestCase


class TestProcessManagers(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def test_all(self):
        # check if the method return the instances (casted to the subclasses).
        processes = Process.objects.all()
        for p in processes:
            self.assertNotEquals(p.__class__, Process)
            self.assertEquals(
                p.__class__,
                Process.objects.get(id=p.pk).type_cast().__class__)

    def test_filter(self):
        # check if the method return the filtered instances (casted to the
        # sublcasses).
        processes = Process.objects.all()
        filtered = Process.objects.filter(id__gt=5)
        self.assertTrue(len(processes) > len(filtered))
        for p in filtered:
            self.assertNotEquals(p.__class__, Process)
            self.assertEquals(
                p.__class__,
                Process.objects.get(id=p.pk).type_cast().__class__)
