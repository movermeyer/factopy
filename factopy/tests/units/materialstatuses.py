# -*- coding: utf-8 -*-
from factopy.models import Stream, Material, MaterialStatus, InvalidStatus
from django.test import TestCase


class TestMaterialStatuses(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.stream = Stream()
        self.stream.save()
        self.second_stream = Stream()
        self.second_stream.save()
        self.material = Material()
        self.material.save()
        self.material_status = MaterialStatus.objects.get_or_create(
            material=self.material,
            stream=self.stream
        )[0]
        self.material_status.save()

    def test_serialization(self):
        material_status = u'%s -> %s' % (
            unicode(self.material_status.stream),
            unicode(self.material_status.material))
        # check if the __str__ method return the created and modified datetime.
        self.assertEquals(str(self.material_status), str(material_status))
        # check if the __unicode__ method is defined to return the created and
        # modified datetime.
        self.assertEquals(unicode(self.material_status), material_status)

    def test_statuses_number(self):
        # check if return the list of statuses indexed by number.
        self.assertEquals(MaterialStatus.statuses_number().keys(), [0, 1, 2])
        self.assertEquals(MaterialStatus.statuses_number().values(),
                          [u'unprocessed', u'processing', u'processed'])

    def test_statuses_name(self):
        # check if return the list of statuses indexed by name.
        self.assertEquals(MaterialStatus.statuses_name().keys(),
                          [u'unprocessed', u'processing', u'processed'])
        self.assertEquals(MaterialStatus.statuses_name().values(), [0, 1, 2])

    def test_clone_for(self):
        # check if the clone method create a new file_status.
        clone = self.material_status.clone_for(self.second_stream)
        self.assertNotEquals(clone, self.material_status)
        # check if the cloned material_status has the second_stream
        # and the same material object.
        self.assertEquals(self.material_status.stream, self.stream)
        self.assertEquals(clone.stream, self.second_stream)
        self.assertEquals(clone.material, self.material_status.material)

    def test_status(self):
        # check if return the status as a name.
        for i, name in MaterialStatus.statuses_number().items():
            self.material_status.state = i
            self.assertEquals(self.material_status.status(), name)

    def test_change_status(self):
        # check if set the right status when use valid ids.
        for name in MaterialStatus.statuses_name().keys():
            self.material_status.change_status(name)
            self.assertEquals(self.material_status.status(), name)
        # check if rise an exception when use invalid ids.
        self.material_status.change_status(u'unprocessed')
        for name in [u'just an invalid status', u'invalid key']:
            with self.assertRaises(InvalidStatus):
                self.material_status.change_status(name)
            self.assertEquals(self.material_status.status(), u'unprocessed')

    def test_processed(self):
        # check if the processed getter return true when the material
        # was processed.
        for name in MaterialStatus.statuses_name().keys():
            self.material_status.change_status(name)
            self.assertEquals(self.material_status.processed,
                              self.material_status.status() == u'processed')
        # check if the processed setter change the processed attribute.
        self.material_status.change_status(u'unprocessed')
        self.assertFalse(self.material_status.processed)
        self.material_status.processed = True
        self.assertEquals(self.material_status.status(), u'processed')
        self.assertTrue(self.material_status.processed)
        self.material_status.processed = False
        self.assertEquals(self.material_status.status(), u'unprocessed')
