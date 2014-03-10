from django.db import models
from polymorphic import PolymorphicModel
import threading


BACKEND_STATE = (
	(0, u'off'),
	(1, u'running'),
)


class InvalidStatus(RuntimeWarning):
	pass


class BackendModel(PolymorphicModel,threading.Thread):
	state = models.IntegerField(choices=BACKEND_STATE, default=0)

	def __init__(self):
		super(BackendModel, self).__init__()
		self._stop = threading.Event()

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()

	def status(self):
		return {x:y for x,y in BACKEND_STATE}[self.state]

	def change_status(self, name):
		try:
			self.state = {y:x for x,y in BACKEND_STATE}[name]
		except KeyError:
			raise InvalidStatus

	def run(self):
		while not self.stopped():
			self.step()
	
	def step(self):
		pass


class Worker(BackendModel):

	def bootup(self):
		if self.status() == u'off':
			self.start()
			self.change_status(u'running')

	def bootdown(self):
		if self.status() == u'running':
			self.stop()
			while not self.stopped(): pass
			self.join()
			self.change_status(u'off')