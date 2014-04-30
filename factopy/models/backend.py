from django.db import models
from polymorphic import PolymorphicModel, PolymorphicManager
import multiprocessing as mp
import time
import Pyro4
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
    ip = models.TextField(default="", null=True)

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
            import socket
            self.ip = socket.gethostbyname(socket.gethostname())
            self.save()
            self.init_stop()
            self.start()
            while not self.is_alive():
                pass
            self.change_status(u'running')

    def bootdown(self):
        if self.status() == u'running':
            self.ip = ""
            self.save()
            self.stop()
            # self.join()
            self.change_status(u'off')

    def is_alive(self):
        sock, result = socket.socket(socket.AF_INET, socket.SOCK_STREAM), False
        try:
            sock.connect((self.ip, 22))
            result = True
        except socket.error:
            pass
        sock.close()
        return result


class Worker(BackendModel):
    class Meta(object):
        app_label = 'factopy'
    identification = models.TextField(default="")
    machine = models.ForeignKey('Machine', null=True)

    def __unicode__(self):
        return u'%s [uri: %s, id: %s, status: %s]' % (
            unicode(self.__class__.__name__),
            unicode(self.machine.uri),
            unicode(self.identification),
            unicode(self.status()))


class Machine(BackendModel):
    class Meta(object):
        app_label = 'factopy'
    uri = models.TextField(default="localhost")
    cluster = models.ForeignKey('Cluster', null=True)

    def __unicode__(self):
        return u'%s [uri: %s, status: %s]' % (
            unicode(self.__class__.__name__),
            unicode(self.uri),
            unicode(self.status()))

    def has_running_workers(self):
        q = self.worker_set.filter(state=BACKEND_STATE.index(u'running'))
        return q.count() > 0

    def start(self):
        super(Machine, self).start()
        for w in self.worker_set.all():
            w.bootup()
        while not self.is_alive() and self.has_running_workers():
            pass

    def stop(self):
        for w in self.worker_set.all():
            w.bootdown()
        super(Machine, self).stop()


class Cluster(BackendModel):
    class Meta(object):
        app_label = 'factopy'


class Node(object):

    def __init__(self):
        self.recognize_network()
        self.configure_pyro4()
        self.configure_node()

    def recognize_network(self):
        import socket
        self.ip = socket.gethostbyname(socket.gethostname())

    def configure_pyro4(self):
        self.is_manager = False
        while not hasattr(self, 'ns'):
            try:
                self.ns = Pyro4.locateNS()
            except Pyro4.errors.NamingError:
                from subprocess import Popen
                self.is_manager = True
                self.ns_process = Popen(
                    'python -m Pyro4.naming -n 0.0.0.0',
                    shell=True)
        print "[ Starting the %s on %s]" % (
            "manager" if self.is_manager else "worker",
            self.ip)
        self.daemon = Pyro4.Daemon()
        self.daemon_process = mp.Process(target=self.daemon.requestLoop)
        self.daemon_process.start()
        self.obtain_cluster()

    def obtain_cluster(self):
        if self.is_manager:
            if not hasattr(self, 'cluster'):
                self.cluster = Cluster.objects.get(pk=1)
                self.cluster.ip = self.ip
                self.cluster.save()
                self.register(self.cluster, "Cluster")
        else:
            while not hasattr(self, 'cluster'):
                try:
                    # self.cluster = Cluster.objects.get(pk=1)
                    self.cluster = self.get("Cluster")
                except Pyro4.errors.NamingError:
                    pass
        return self.cluster

    def register(self, object, name):
        self.ns.register(name, self.daemon.register(object))

    def get(self, name):
        return Pyro4.Proxy("PYRONAME:"+name)

    def configure_node(self):
        print "0"
        if self.is_manager:
            self.node = self.cluster
        else:
            print "0a"
            self.node = self.get_machine()
            print "1"
            if self.node:
                print "2"
                print unicode(self.node.uri)
                print self.is_manager
                self.register(self.node, self.node.uri)
        print "3"
        print unicode(self.node)
        if self.node.status() == u'running':
            raise KeyboardInterrupt("Worker booted up previously.")
        self.node.bootup()

    def get_machine(self):
        print self.cluster.machine_set.filter(ip=self.ip)
        machines = self.cluster.machine_set.filter(ip=self.ip)
        print "->", machines
        return machines[0] if len(machines) > 0 else None

    def bootup(self):
        self.node.bootup()

    def bootdown(self):
        self.node.bootdown()
        # self.cluster.bootdown()
        # if self.is_manager:
        #    raise KeyboardInterrupt('This IP is not assigned to the cluster.')

    def __del__(self):
        # Terminate the name server process
        if hasattr(self, 'ns_process'):
            self.ns_process.terminate()
            self.daemon_process.terminate()
