from django.db import models
from polymorphic import PolymorphicModel, PolymorphicManager
import multiprocessing as mp
import time


BACKEND_STATE = (
	(0, u'off'),
	(1, u'running'),
)


class InvalidStatus(RuntimeWarning):
	pass


class BackendModel(PolymorphicModel,mp.Process):
	class Meta(object):
		app_label = 'factopy'
	objects = PolymorphicManager()
	state = models.IntegerField(choices=BACKEND_STATE, default=0)

	def init_stop(self):
		if not hasattr(self,'_stop'):
			self._stop = mp.Event()

	def stop(self):
		# The second time terminate the process
		if self.stopped():
			self.terminate()
		self._stop.set()

	def stopped(self):
		self.init_stop()
		return self._stop.is_set()

	def status(self):
		return {x:y for x,y in BACKEND_STATE}[self.state]

	def change_status(self, name):
		try:
			self.state = {y:x for x,y in BACKEND_STATE}[name]
			self.save()
		except KeyError:
			raise InvalidStatus

	def run(self):
		while not self.stopped():
			self.step()
			time.sleep(0.1)
		return

	def step(self):
		pass

	def bootup(self):
		if self.status() == u'off':
			self.init_stop()
			self.start()
			while not self.is_alive(): pass
			self.change_status(u'running')

	def bootdown(self):
		if self.status() == u'running':
			self.stop()
			#self.join()
			self.change_status(u'off')


class Worker(BackendModel):
	class Meta(object):
		app_label = 'factopy'
	machine = models.ForeignKey('Machine', null=True)


class Machine(BackendModel):
	class Meta(object):
		app_label = 'factopy'

	def start(self):
		super(Machine, self).start()
		for w in self.worker_set.all():
			w.bootup()
		while not self.is_alive() and len([w for w in self.worker_set.all() if w.status() == u'running']): pass

	def stop(self):
		for w in self.worker_set.all():
			w.bootdown()
		super(Machine, self).stop()