from django.db import models
from polymorphic import PolymorphicModel, PolymorphicManager
import multiprocessing as mp
import signal
import threading as th
import socket
from factopy.models import InvalidStatus, Stream


BACKEND_STATE = (
    (0, u'off'),
    (1, u'booting'),
    (2, u'running'),
)


class InvalidBackendModel(Exception):
    pass


class NetworkInterrupt(Exception):
    pass


class BackendModel(PolymorphicModel, th.Thread):
    class Meta(object):
        app_label = 'factopy'
    objects = PolymorphicManager()
    state = models.IntegerField(choices=BACKEND_STATE, default=0)

    @classmethod
    def statuses_number(klass):
        return {x: y for x, y in BACKEND_STATE}

    @classmethod
    def statuses_name(klass):
        return {y: x for x, y in BACKEND_STATE}

    def __str__(self):
        return unicode(BackendModel.objects.get(id=self.id)).encode("utf-8")

    def __unicode__(self):
        return u'%s [status: %s]' % (
            unicode(self.__class__.__name__),
            unicode(self.status()))

    def init_stop(self):
        if not hasattr(self, '_stop'):
            self._stop = th.Event()

    def stop(self):
        self.change_status(u'off')
        self._stop.set()

    def sync_stop(self):
        if self.status() == u'off':
            self.stop()

    def stopped(self):
        self.init_stop()
        self.sync_stop()
        return self._stop.is_set()

    def status(self):
        self.state = self.__class__.objects.get(id=self.id).state
        return self.__class__.statuses_number()[self.state]

    def change_status(self, name):
        try:
            self.state = self.__class__.statuses_name()[name]
            self.save()
        except KeyError:
            raise InvalidStatus

    def start(self):
        self.change_status(u'running')
        super(BackendModel, self).start()

    def run(self):
        while not self.stopped():
            try:
                self.step()
            except Exception, error:
                raise InvalidBackendModel(error)

    def bootup(self):
        if self.status() == u'off':
            self.start()

    def bootdown(self):
        if self.status() == u'running':
            self.stop()
            self.join()


import time
# from django.db import transaction


# @transaction.commit_on_success
def manager_job(args):
    ss = Stream.requiring_work().count()
    # transaction.set_dirty()
    # if ss.count() > 0:
    return u'%f.1->%s (%s)' % (time.clock(), args, unicode(ss))
    # else:
    #    return None


class Node(BackendModel):
    class Meta(object):
        app_label = 'factopy'
    ip = models.TextField(default="", null=True)
    manager_amount = models.IntegerField(default=2)

    def bootup(self):
        if self.status() == u'off':
            self.ip = socket.gethostbyname(socket.gethostname())

            def init_manager():
                signal.signal(signal.SIGINT, signal.SIG_IGN)
            self.managers = mp.Pool(self.manager_amount, init_manager)
        super(Node, self).bootup()

    def bootdown(self):
        if hasattr(self, 'managers'):
            try:
                self.managers.close()
            except KeyboardInterrupt:
                self.managers.terminate()
        super(Node, self).bootdown()

    def step(self):
        print self.managers.map(manager_job, range(6))
