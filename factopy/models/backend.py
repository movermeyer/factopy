from django.db import models
from polymorphic import PolymorphicModel, PolymorphicManager
import multiprocessing as mp
import signal
import threading as th
import socket
from factopy.models import InvalidStatus, Stream
from django.db import connection


BACKEND_STATE = (
    (0, u'off'),
    (1, u'booting'),
    (2, u'running'),
)


class StoppableThread(th.Thread):

    def __init__(self, model):
        super(StoppableThread, self).__init__()
        self._stop = th.Event()
        self.model = model
        self.opts = {
            u'off': self._stop.set,
            u'running': self._stop.clear}
        self.sync_stop()

    def start(self):
        self.model.bootup()
        self.model.change_status(u'running')
        super(StoppableThread, self).start()

    def stop(self):
        self.model.bootdown()
        self.model.change_status(u'off')
        self._stop.set()

    def sync_stop(self):
        self.opts[self.model.status()]()

    def stopped(self):
        self.sync_stop()
        return self._stop.is_set()

    def run(self):
        while not self.stopped():
            try:
                self.model.step()
            except AssertionError:
                self.stop()


class BackendModel(PolymorphicModel):
    class Meta(object):
        app_label = 'factopy'
    objects = PolymorphicManager()
    state = models.IntegerField(choices=BACKEND_STATE, default=0)

    @classmethod
    def statuses_number(cls):
        return {x: y for x, y in BACKEND_STATE}

    @classmethod
    def statuses_name(cls):
        return {y: x for x, y in BACKEND_STATE}

    def __str__(self):
        return unicode(BackendModel.objects.get(id=self.id)).encode("utf-8")

    def __unicode__(self):
        return u'%s [status: %s]' % (
            unicode(self.__class__.__name__),
            unicode(self.status()))

    def status(self):
        self.state = self.__class__.objects.get(id=self.id).state
        return self.__class__.statuses_number()[self.state]

    def change_status(self, name):
        try:
            self.state = self.__class__.statuses_name()[name]
            self.save()
        except KeyError:
            raise InvalidStatus

    def step(self):
        raise Exception(u'Subclass responsability')

    def bootup(self):
        pass

    def bootdown(self):
        pass


def manager_job(stream_id):
    stream, is_new = Stream.objects.get_or_create(id=stream_id)
    if is_new:
        raise Exception(u'Trying to process a recently created Stream object.')
    process = stream.feed
    process.step()
    return u'%i->%s (%s)' % (
        stream_id,
        unicode(stream.unprocessed_count),
        stream.feed.name)


class Node(BackendModel):
    class Meta(object):
        app_label = 'factopy'
    ip = models.TextField(default="", null=True)
    manager_amount = models.IntegerField(default=2)

    def init_managers(self):
        self.managers = mp.Pool(self.manager_amount, lambda: signal.signal(
                                signal.SIGINT, signal.SIG_IGN))

    def bootup(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.init_managers()

    def step(self):
        ids = Stream.requiring_work().values_list('id', flat=True)
        # here the map function should not return any value.
        self.managers.map(manager_job, ids)
        connection.close()
