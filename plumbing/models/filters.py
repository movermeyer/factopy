from core import Process


class Filter(Process):
	class Meta(object):
		app_label = 'plumbing'

	def should_be_cloned(self, material_status):
		return False

	def do(self, stream):
		resultant_stream = stream.clone()
		for fs in stream.materials.all():
			if self.should_be_cloned(fs):
				fs.clone_for(resultant_stream)
			fs.processed=True
			fs.save()
		return resultant_stream

	def mark_with_tags(self, stream):
		# Don't used because these process is transparent in the name
		pass