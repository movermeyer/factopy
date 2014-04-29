from core import Process


class Collect(Process):
    class Meta(object):
        app_label = 'factopy'

    def get_key(self, material_status):
        raise AttributeError("'Collect' object has no attribute 'get_key'")

    def get_keys(self, stream):
        return set([ self.get_key(fs) for fs in stream.materials.all() ])

    def init_empty_streams(self, stream):
        keys = self.get_keys(stream)
        resultant_stream = {}
        for k in keys:
            resultant_stream[k] = stream.clone()
        return resultant_stream

    def do(self, stream):
        resultant_stream = self.init_empty_streams(stream)
        for fs in stream.materials.all():
            fs.clone_for(resultant_stream[self.get_key(fs)])
            fs.processed=True
            fs.save()
        for k in resultant_stream.keys():
            resultant_stream[k].tags.append(k)
        return resultant_stream.values()

    def mark_with_tags(self, stream):
        # Don't used because these process always return multiple streams
        pass