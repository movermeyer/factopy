from django.db import models
from polymorphic import PolymorphicModel, PolymorphicManager
from datetime import datetime
import pytz


class TagManager(models.Model):
    class Meta(object):
        app_label = 'factopy'
    tag_string = models.TextField(db_index=True, default="")

    @classmethod
    def create_empty(klass):
        tm = klass()
        tm.save()
        return tm

    def exist(self, tag):
        return tag in self.list()

    def list(self):
        l = self.tag_string.split(",")
        if u"" in l:
            l.remove(u"")
        return l

    def empty(self):
        return self.list() == []

    def insert_first(self, tag):
        if not self.exist(tag):
            self.tag_string = ((tag + "," + self.tag_string)
                               if len(self.tag_string) > 0 else tag)
            self.save()

    def append(self, tag):
        if not self.exist(tag):
            self.tag_string += ("," + tag) if len(self.tag_string) > 0 else tag
            self.save()

    def clone(self):
        t = TagManager(tag_string=self.tag_string)
        t.save()
        return t

    def make_filename(self):
        return ".".join(self.list())

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return u'[%s]' % self.tag_string


class Stream(models.Model, object):
    class Meta(object):
        app_label = 'factopy'
    tags = models.ForeignKey(TagManager, related_name='stream',
                             default=TagManager.create_empty)
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
    def requiring_work(klass):
        q = klass.objects.extra(select={
            'unprocessed_count': "unprocessed_count > '0'"
        })
        q = q.extra(order_by=['-unprocessed_count'])
        return q

    @classmethod
    def create_empty(klass):
        s = klass()
        s.save()
        return s

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return u'[id: %s tags: %s unprocessed: %s] -> %s' % (
            unicode(self.pk),
            unicode(self.tags),
            unicode(self.unprocessed_count),
            unicode(self.feed))

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.tags.save()
        if not self.pk:
            self.created = now
        self.modified = now
        return super(Stream, self).save(*args, **kwargs)

    def clone(self):
        t = self.tags.clone()
        t.save()
        s = Stream(tags=t)
        s.save()
        return s

    def unprocessed(self):
        return self.materials.filter(processed=False)

    def empty(self):
        pending = self.unprocessed()
        return len(pending) == 0


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


class MaterialStatus(models.Model):
    class Meta(object):
        app_label = 'factopy'
        verbose_name_plural = 'Material statuses'
        unique_together = ("material", "stream")
    material = models.ForeignKey('Material', related_name='stream')
    stream = models.ForeignKey(Stream, related_name='materials')
    processed = models.BooleanField()

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return u'%s -> %s' % (unicode(self.stream), unicode(self.material))

    def clone_for(self, stream):
        cloned_material_status = MaterialStatus(material=self.material,
                                                stream=stream)
        cloned_material_status.save()
        return cloned_material_status


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

    def mark_with_tags(self, stream):
        pass

    def notify(self, stream):
        self.observers.add(stream)

    def not_notify(self, stream):
        self.observers.add(stream)
