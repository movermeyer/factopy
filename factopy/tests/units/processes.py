# -*- coding: utf-8 -*-
from factopy.models import Stream, Process
from django.test import TestCase


class TestProcesses(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.process = Process.objects.get(name='year.Mmonth')
        self.other_process = Process.objects.get(pk=6)
        self.last_process = Process(
            name='Testing',
            description='This is a fake process only for testing.')
        self.stream = Stream()

    def test_serialization(self):
        # check if the __str__ method is defined to return the class name with
        # the name parameter.
        process = u'Filter [year.Mmonth]'
        other_process = u"Filter [Filter night's images]"
        self.assertEquals(str(self.process), str(process))
        self.assertEquals(str(self.other_process), str(other_process))
        # check if the __unicode__ method is defined to return the class name
        # with the name parameter.
        self.assertEquals(unicode(self.process), process)
        self.assertEquals(unicode(self.other_process), other_process)
