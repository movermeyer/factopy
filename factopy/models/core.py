from django.db import models
from polymorphic import PolymorphicModel, PolymorphicManager
from datetime import datetime
import pytz


class Stream(models.Model, object):
    class Meta(object):
        app_label = 'factopy'
    unprocessed_count = models.IntegerField(default=0)
    observe = models.ManyToManyField('Process',
                                     related_name='observers',
                                     blank=True)
    feed = models.ForeignKey('Process', related_name='streams', null=True)
    created = models.DateTimeField(
        editable=False,
        default=datetime.utcnow().replace(tzinfo=pytz.UTC))
    modified = models.DateTimeField(
        default=datetime.utcnow().replace(tzinfo=pytz.UTC))

    @classmethod
    def requiring_work(cls):
        q = cls.objects.filter(unprocessed_count__gt=0)
        q = q.extra(order_by=['-unprocessed_count'])
        return q

    @classmethod
    def create_empty(cls):
        s = cls()
        s.save()
        return s

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return u'[id: %s unprocessed: %s] -> %s' % (
            unicode(self.pk),
            unicode(self.unprocessed_count),
            unicode(self.feed))

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        if not self.pk:
            self.created = now
        self.modified = now
        return super(Stream, self).save(*args, **kwargs)

    def clone(self):
        s = Stream()
        s.save()
        return s

    def unprocessed(self):
        return self.materials.filter(
            state=MaterialStatus.statuses_name()[u'unprocessed'])

    def empty(self):
        pending = self.unprocessed()
        return len(pending) == 0

    def update_unprocessed_count(self):
        unprocessed = MaterialStatus.statuses_name()[u'unprocessed']
        self.unprocessed_count = self.materials\
            .filter(state=unprocessed).count()
        self.save()


class Material(PolymorphicModel, object):
    class Meta(object):
        app_label = 'factopy'
    objects = PolymorphicManager()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return unicode(Material.objects.get(id=self.id)).encode("utf-8")

    def __unicode__(self):
        return u'(created: %s, modified: %s)' % (
            unicode(self.created),
            unicode(self.modified))

    def inject_into(self, stream):
        material_status = MaterialStatus(material=self,
                                         stream=stream)
        material_status.change_status(u"unprocessed")
        material_status.save()
        return material_status


MATERIAL_STATE = (
    (0, u'unprocessed'),
    (1, u'processing'),
    (2, u'processed')
)


class InvalidStatus(RuntimeWarning):
    pass


class MaterialStatus(models.Model):
    class Meta(object):
        app_label = 'factopy'
        verbose_name_plural = 'Material statuses'
        unique_together = ("material", "stream")
    material = models.ForeignKey('Material', related_name='stream')
    stream = models.ForeignKey(Stream, related_name='materials')
    state = models.IntegerField(choices=MATERIAL_STATE, default=0)

    @classmethod
    def statuses_number(cls):
        return {x: y for x, y in MATERIAL_STATE}

    @classmethod
    def statuses_name(cls):
        return {y: x for x, y in MATERIAL_STATE}

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return u'%s -> %s' % (unicode(self.stream), unicode(self.material))

    def clone_for(self, stream):
        return self.material.inject_into(stream)

    def status(self):
        return self.__class__.statuses_number()[self.state]

    def change_status(self, name):
        try:
            self.state = self.__class__.statuses_name()[name]
            self.stream.update_unprocessed_count()
            self.save()
        except KeyError:
            raise InvalidStatus

    @property
    def processed(self):
        return self.status() == u'processed'

    @processed.setter
    def processed(self, value):
        state = u'unprocessed'
        if value:
            state = u'processed'
        self.change_status(state)


class Process(PolymorphicModel, object):
    class Meta(object):
        app_label = 'factopy'
        verbose_name_plural = 'Processes'
    objects = PolymorphicManager()
    name = models.TextField(db_index=True)
    description = models.TextField(db_index=True)

    def __str__(self):
        return unicode(Process.objects.get(id=self.id)).encode("utf-8")

    def __unicode__(self):
        return u'%s [%s]' % (
            self.__class__.__name__,
            self.name)

    def step(self):
        raise Exception(u"Subclass responsability")

    def notify(self, material):
        for observer in self.observers.all():
            material.inject_into(observer)
