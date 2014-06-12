from core import Process


class Filter(Process):
    class Meta(object):
        app_label = 'factopy'

    def should_be_cloned(self, material_status):
        return False

    def step(self):
        for stream in self.streams.all():
            for material_status in stream.unprocessed():
                material_status.change_status(u'processing')
                if self.should_be_cloned(material_status):
                    self.notify(material_status.material)
                material_status.change_status(u'processed')
