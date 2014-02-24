from django.db import models
from core import Process, Stream
import threading


class Adapt(Process):
	class Meta(object):
		app_label = 'factopy'
	stream = models.ForeignKey(Stream, null=True, default=None)

	def do(self, stream):
		return stream

	def update(self):
		raise Exception("Subclass responsability")


class Importer(Adapt):
	class Meta(object):
			app_label = 'factopy'
	frequency = models.IntegerField(default=15*60) # It is expressed in seconds

	@classmethod
	def setup_unloaded(klass):
		importers = [ i for i in klass.objects.all() if not hasattr(i,"thread") ]
		for i in importers:
			i.thread = threading.Timer(i.frequency, i.update)
			i.thread.start()
		return importers