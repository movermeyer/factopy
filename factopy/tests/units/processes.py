# -*- coding: utf-8 -*-
from factopy.models import Stream, Process
from django.test import TestCase


class TestProcesses(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.process = Process.objects.get(name='Execute model')
        self.other_process = Process.objects.get(pk=4)
        self.last_process = Process(
            name='Testing',
            description='This is a fake process only for testing.')
        self.stream = Stream()

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
        with self.assertRaises(Exception) as e:
            self.process.step()
        self.assertEquals(unicode(e.exception), u'Subclass responsability')
