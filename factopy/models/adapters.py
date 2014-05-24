from django.db import models
from core import Process
import threading
from datetime import datetime, timedelta
import pytz


class Adapt(Process):
    class Meta(object):
        app_label = 'factopy'

    def step(self):
        if self.should_adapt():
            self.update()

    def should_adapt(self):
        return False

    def update(self):
        raise Exception(u"Subclass responsability")


class Push(Adapt):
    class Meta(object):
            app_label = 'factopy'
    frequency = models.IntegerField(default=15*60)  # expressed in seconds
    previous = models.DateTimeField(default=datetime.utcnow().
                                    replace(tzinfo=pytz.UTC))

    @classmethod
    def setup_unloaded(cls):
        pushers = [i for i in cls.objects.all()
                   if not hasattr(i, "thread")]
        for i in pushers:
            i.thread = threading.Timer(i.frequency, i.update)
            i.thread.start()
        return pushers

    def should_adapt(self):
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        should_push = (now - self.previous) > timedelta(seconds=self.frequency)
        if should_push:
            self.previous = now
        return should_push
