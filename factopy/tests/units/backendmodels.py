# -*- coding: utf-8 -*-
from factopy.models import BackendModel, InvalidStatus
from django.test import TestCase


class TestBackendModels(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.model = BackendModel.objects.get(pk=1)

    def test_serialization(self):
        # check if the __str__ method is defined to return the class name with
        # the status.
        model = u"Node [status: off]"
        self.assertEquals(str(self.model), str(model))
        # check if the __unicode__ method is defined to return the class name
        # with the status.
        self.assertEquals(unicode(self.model), model)

    def test_status(self):
        # check if the model status is off.
        self.assertTrue(self.model.status(), u'off')
        self.model.state = 1
        # check if the model status is running.
        self.assertTrue(self.model.status(), u'running')

    def test_change_status(self):
        # check if the model status is off.
        self.assertTrue(self.model.status(), u'off')
        self.model.change_status(u'running')
        # check if the model status is running.
        self.assertTrue(self.model.status(), u'running')
        # check if an unknown status rais an exception
        with self.assertRaises(InvalidStatus):
            self.model.change_status(u'jumping')
