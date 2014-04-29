from django.db import models
from polymorphic import PolymorphicModel, PolymorphicManager
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import datetime
import pytz
from itertools import tee, izip
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


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
		if u"" in l: l.remove(u"")
		return l

	def empty(self):
		return self.list() == []

	def insert_first(self, tag):
		if not self.exist(tag):
			self.tag_string = (tag + "," + self.tag_string)  if len(self.tag_string) > 0 else tag
			self.save()

	def append(self,tag):
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


class Stream(models.Model,object):
	class Meta(object):
		app_label = 'factopy'
	tags = models.ForeignKey(TagManager, related_name='stream', default=TagManager.create_empty)
	unprocessed_count = models.IntegerField(default=0)
	feed = models.ForeignKey('Process', related_name='streams', null=True)
	created = models.DateTimeField(editable=False,default=datetime.utcnow().replace(tzinfo=pytz.UTC))
	modified = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=pytz.UTC))

	@classmethod
	def requiring_work(klass):
		q = klass.objects.extra(select={'unprocessed_count': "unprocessed_count > '0'"})
		q = q.extra(order_by = ['-unprocessed_count'])
		return q

	@classmethod
	def create_empty(klass):
		s = klass()
		s.save()
		return s

	def __str__(self):
		return unicode(self).encode("utf-8")

	def __unicode__(self):
		return u'%s %s' % (unicode(self.pk), unicode(self.tags))

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
		return u'(created: %s, modified: %s)' % (unicode(self.created), unicode(self.modified))


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
		cloned_material_status = MaterialStatus(material=self.material,stream=stream)
		cloned_material_status.save()
		return cloned_material_status


class Process(PolymorphicModel,object):
	class Meta(object):
		app_label = 'factopy'
		verbose_name_plural = 'Processes'
	objects = PolymorphicManager()
	name = models.TextField(db_index=True)
	description = models.TextField(db_index=True)
	observed = models.ManyToManyField(Stream,related_name='observe',blank=True)

	def __str__(self):
		return unicode(Process.objects.get(id=self.id)).encode("utf-8")

	def __unicode__(self):
		return u'%s [%s]' % (self.__class__.__name__, self.name)

	def mark_with_tags(self, stream):
		pass


class ComplexProcess(Process):
	class Meta(object):
		app_label = 'factopy'
	processes = models.ManyToManyField('Process', through='ProcessOrder', related_name='complex_process')

	def encapsulate_in_array(self, streams):
		if not streams.__class__ in [list, tuple]:
			streams = [ streams ]
		return streams

	def get_ordered_subprocesses(self):
		return self.processes.all().order_by('used_by__position')

	def do(self, stream):
		ps = self.get_ordered_subprocesses()
		for subprocess in ps:
			stream = self.encapsulate_in_array(stream)
			tmp_results = []
			for s in stream:
				if not s.empty():
					result = subprocess.do(s)
					subprocess.mark_with_tags(s)
					tmp_results += self.encapsulate_in_array(result)
			stream = tmp_results
		return stream

	def update_wires(self, method):
		ps = self.get_ordered_subprocesses()
		if ps.count() > 0:
			# input wires
			if self.streams.count():
				getattr(ps[0].observed, method)(self.streams.all()[0])
			# internal wires
			for p1, p2 in pairwise(ps):
				getattr(p1.observed,method)(p2.streams.all()[0])
			# output wires
			last = ps.reverse()[0]
			for o in self.observed.all():
				getattr(last.observed,method)(o)

@receiver(pre_save, sender=ComplexProcess)
def unwire(sender, instance, *args, **kwargs):
	instance.update_wires('remove')

@receiver(post_save, sender=ComplexProcess)
def wire(sender, instance, *args, **kwargs):
	instance.update_wires('add')


class ProcessOrder(models.Model):
	class Meta(object):
		app_label = 'factopy'
	position = models.IntegerField()
	process = models.ForeignKey('Process', related_name='used_by')
	complex_process = models.ForeignKey(ComplexProcess)

	def __str__(self):
		return unicode(self).encode("utf-8")

	def __unicode__(self):
		return unicode(self.process)