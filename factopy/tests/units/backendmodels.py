# -*- coding: utf-8 -*-
from factopy.models import BackendModel, InvalidStatus
from django.test import TestCase


class TestBackendModels(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.model = BackendModel()
        self.model.save()

    def tearDown(self):
        self.model.change_status(u'off')
        self.model.delete()

    def test_serialization(self):
        # check if the __str__ method is defined to return the class name with
        # the status.
        model = u"BackendModel [status: off]"
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

    def test_bootdown(self):
        # check if the bootdown exists.
        self.assertTrue(hasattr(self.model, 'bootdown'))

    def test_step(self):
        # check if the abstract model raise an exception.
        self.model.bootup()
        with self.assertRaises(Exception) as e:
            self.model.step()
        self.assertEquals(unicode(e.exception), u'Subclass responsability')
        self.model.bootdown()
