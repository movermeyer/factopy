# -*- coding: utf-8 -*-
from factopy.models import Material, MaterialStatus, Stream
from django.test import TestCase


class TestMaterials(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.material = Material()
        self.material.save()
        self.other_material = Material()
        self.other_material.save()
        self.stream = Stream()
        self.stream.save()

    def test_serialization(self):
        material = u'(created: %s, modified: %s)' % (
            unicode(self.material.created),
            unicode(self.material.modified))
        other_material = u'(created: %s, modified: %s)' % (
            unicode(self.other_material.created),
            unicode(self.other_material.modified))
        # check if the __str__ method return the created and modified datetime.
        self.assertEquals(str(self.material), str(material))
        self.assertEquals(str(self.other_material), str(other_material))
        # check if the __unicode__ method is defined to return the created and
        # modified datetime.
        self.assertEquals(unicode(self.material), material)
        self.assertEquals(unicode(self.other_material), other_material)

    def test_inject_into(self):
        # check if the inject_into method create a new file_status.
        material_status = self.material.inject_into(self.stream)
        self.assertEquals(material_status.__class__, MaterialStatus)
        # check if the new material_status has the same stream, the same
        # material object and the unprocessed state.
        self.assertEquals(material_status.stream, self.stream)
        self.assertEquals(material_status.material, self.material)
        self.assertEquals(material_status.status(), u'unprocessed')
