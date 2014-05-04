from django.db import models
from polymorphic import PolymorphicModel, PolymorphicManager
import multiprocessing as mp
import time
import socket


BACKEND_STATE = (
    (0, u'off'),
    (1, u'running'),
)


class InvalidStatus(RuntimeWarning):
    pass


class BackendModel(PolymorphicModel, mp.Process):
    class Meta(object):
        app_label = 'factopy'
    objects = PolymorphicManager()
    state = models.IntegerField(choices=BACKEND_STATE, default=0)

    def __str__(self):
        return unicode(BackendModel.objects.get(id=self.id)).encode("utf-8")

    def __unicode__(self):
        return u'%s [status: %s]' % (
            unicode(self.__class__.__name__),
            unicode(self.status()))

    def init_stop(self):
        if not hasattr(self, '_stop'):
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
        return {x: y for x, y in BACKEND_STATE}[self.state]

    def change_status(self, name):
        try:
            self.state = {y: x for x, y in BACKEND_STATE}[name]
            self.save()
        except KeyError:
            raise InvalidStatus

    def run(self):
        try:
            while not self.stopped():
                self.step()
                time.sleep(0.1)
        except:
            pass
        return

    def step(self):
        pass

    def bootup(self):
        if self.status() == u'off':
            self.init_stop()
            self.start()
            self.change_status(u'running')

    def bootdown(self):
        if self.status() == u'running':
            self.ip = ""
            self.save()
            self.stop()
            # self.join()
            self.change_status(u'off')


class Worker(BackendModel):
    class Meta(object):
        app_label = 'factopy'
    identification = models.TextField(default="")
    node = models.ForeignKey('Node', null=True)

    def __unicode__(self):
        return u'%s [id: %s, status: %s]' % (
            unicode(self.__class__.__name__),
            unicode(self.identification),
            unicode(self.status()))


class Node(BackendModel):
    class Meta(object):
        app_label = 'factopy'
    ip = models.TextField(default="", null=True)

    def bootup(self):
        if self.status() == u'off':
            self.ip = socket.gethostbyname(socket.gethostname())
            self.save()
            super(Node, self).bootup()
