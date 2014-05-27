from django.core.management.base import BaseCommand
from factopy.models import StoppableThread, Node
import sys


class Command(BaseCommand, object):
    args = ''
    help = ('Run the background process that download the active '
            'AutomaticDownload instances.')

    def __init__(self, *args, **options):
        super(Command, self).__init__(*args, **options)
        self.node = Node.objects.all()[0]
        self.thread = StoppableThread(self.node)

    def handle(self, *args, **options):
        import time
        print 'Press Ctrl+C'
        try:
            self.thread.start()
            while not self.thread.stopped():
                time.sleep(10)
            print "Shutdown by network..."
        except KeyboardInterrupt:
            print "Shutdown by keyboard..."
        self.thread.stop()
        self.thread.join(1)
        if self.thread.is_alive():
            self.thread.kill()
        sys.exit(0)
