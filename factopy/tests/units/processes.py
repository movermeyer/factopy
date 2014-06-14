# -*- coding: utf-8 -*-
from factopy.models import Process, Material
from django.test import TestCase


class TestProcesses(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.process = Process.objects.get(name='Execute model')
        self.other_process = Process.objects.get(pk=4)
        self.observed_process = Process.objects.get(name='Grow database')

    def test_serialization(self):
        # check if the __str__ method is defined to return the class name with
        # the name parameter.
        process = u'Process [Execute model]'
        other_process = u"Filter [Filter materials]"
        self.assertEquals(str(self.process), str(process))
        self.assertEquals(str(self.other_process), str(other_process))
        # check if the __unicode__ method is defined to return the class name
        # with the name parameter.
        self.assertEquals(unicode(self.process), process)
        self.assertEquals(unicode(self.other_process), other_process)

    def test_step(self):
        # check if the abstract clas rise the Subclass responsability
        # exception.
        with self.assertRaisesRegexp(Exception, u'Subclass responsability'):
            self.process.step()

    def test_notify(self):
        # check that the observers not contains the material.
        material = Material.objects.get(pk=1)
        materials = [ms.material for s in self.observed_process.observers.all()
                     for ms in s.materials.all()]
        self.assertNotIn(material, materials)
        # check if notify send to all the observers the material.
        self.observed_process.notify(material)
        for s in self.observed_process.observers.all():
            self.assertIn(material, [ms.material for ms in s.materials.all()])
