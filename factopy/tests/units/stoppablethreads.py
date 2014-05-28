# -*- coding: utf-8 -*-
from factopy.models import BackendModel, StoppableThread
from django.test import TestCase
import threading as th
from defer import defer


class TestStoppableThreads(TestCase):
    fixtures = ['initial_data.yaml', '*']

    def setUp(self):
        self.model = BackendModel.objects.get(pk=1)
        self.thread = StoppableThread(self.model)

    def tearDown(self):
        if self.thread.is_alive():
            self.thread.stop()
            self.thread.join()

    def test_init(self):
        # check that the _stop attr is there when the object was initialized.
        self.assertTrue(hasattr(self.thread, '_stop'))
        self.assertTrue(hasattr(self.thread, 'model'))
        self.assertTrue(hasattr(self.thread, 'opts'))
        for k in [u'off', u'running']:
            self.assertIn(k, self.thread.opts.keys())
        self.assertEquals(self.model.status(), u'off')

    def test_start(self):
        # check if status, threading count and if is_alive change when
        # start the thread.
        self.assertEquals(self.model.status(), u'off')
        self.assertFalse(self.thread.is_alive())
        old_count = th.active_count()
        self.thread.start()
        new_count = th.active_count()
        self.assertTrue(self.thread.is_alive())
        self.assertEquals(self.model.status(), u'running')
        self.assertTrue(new_count > old_count)

    def test_stop(self):
        self.thread.start()
        # check if status, threading_count and if is_alive change when
        # stop the thread.
        self.assertEquals(self.model.status(), u'running')
        self.assertTrue(self.thread.is_alive())
        old_count = th.active_count()
        self.thread.stop()
        self.thread.join()
        new_count = th.active_count()
        self.assertEquals(self.model.status(), u'off')
        self.assertFalse(self.thread.is_alive())
        self.assertTrue(new_count < old_count)

    def test_sync_stop(self):
        # check if sync stop not change when syncrhonizes to the same state.
        self.assertEquals(self.model.status(), u'off')
        self.assertTrue(self.thread._stop.is_set())
        self.model.change_status(u'off')
        self.thread.sync_stop()
        self.assertEquals(self.model.status(), u'off')
        self.assertTrue(self.thread._stop.is_set())
        # check if sync stop synchronizes when change the state.
        self.model.change_status(u'running')
        self.thread.sync_stop()
        self.assertFalse(self.thread._stop.is_set())
        # before change the state, test if don't change when set the
        # to running again.
        self.model.change_status(u'running')
        self.thread.sync_stop()
        self.assertFalse(self.thread._stop.is_set())
        # continue with the test changing to off
        self.model.change_status(u'off')
        self.thread.sync_stop()
        self.assertTrue(self.thread._stop.is_set())

    def test_stopped(self):
        # check if return the _stop attr value synchronized with the status.
        self.assertTrue(self.thread.stopped())
        self.model.change_status(u'running')
        self.assertFalse(self.thread.stopped())
        self.model.change_status(u'off')
        self.assertTrue(self.thread.stopped())

    def test_run(self):
        # check if the run method contain the backend main loop.
        self.count = 0

        def wrap():
            self.count = self.count + 1
            if self.count > 3:
                self.thread.stop()
        self.thread.model.step = wrap
        self.thread._stop.clear()
        self.model.change_status(u'running')
        self.assertFalse(self.thread.stopped())
        defer(lambda: self.thread.run())
        self.assertTrue(self.count > 3)
