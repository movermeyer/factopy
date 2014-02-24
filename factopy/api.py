from factopy.models import Stream, Material, MaterialStatus, Process
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource


class PolymorphicModelResource(ModelResource,object):
	def get_class_name(self, bundle):
		return unicode(bundle.obj.__class__.__name__).lower()
	def extend_key(self, dictionary, key, subdictionary):
		if not key in dictionary: dictionary[key] = {}
		dictionary[key] = dict(dictionary[key].items() + subdictionary.items())
	def deserialize(self, obj):
		return dict((attr, obj.__dict__[attr]) for attr in obj.__dict__ if not (attr[-3:] == '_id' or attr in ['_state']))
	def add_foreign_keys(self, bundle, foreign_keys):
		foreign_keys.remove('polymorphic_ctype_id')
		ids = [ fk for fk in foreign_keys if not fk[-len('_ptr_id'):] == '_ptr_id' ]
		return dict((k[:-3],self.deserialize(getattr(bundle.obj,k[:-3]))) for k in ids)
	def dehydrate(self, bundle):
		class_name = self.get_class_name(bundle)
		bundle = super(PolymorphicModelResource,self).dehydrate(bundle)
		foreign_keys = [ k for k in bundle.obj.__dict__.keys() if k[-len('_id'):] == '_id' ]
		keys = [ unicode(k) for k in bundle.data.keys() + [ '_state', 'polymorphic_ctype_id' ] + foreign_keys ]
		extras = dict((k,v) for k,v in bundle.obj.__dict__.iteritems() if not unicode(k) in keys )
		self.extend_key(bundle.data, class_name, extras)
		self.extend_key(bundle.data, class_name, self.add_foreign_keys(bundle, foreign_keys))
		return bundle


class MaterialResource(PolymorphicModelResource):
	class Meta(object):		
		queryset = Material.objects.all()
		resource_name = 'material'
		filtering = {
			'created': ['exact', 'lt', 'lte', 'gte', 'gt'],
			'modified': ['exact', 'lt', 'lte', 'gte', 'gt'],
		}
		authentication = SessionAuthentication()


class MaterialStatusResource(ModelResource):
	material = fields.ForeignKey(MaterialResource, 'material', full=True)
	class Meta(object):
		queryset = MaterialStatus.objects.all()
		resource_name = 'material_status'
		authentication = SessionAuthentication()


class StreamResource(ModelResource):
	class Meta(object):
		queryset = Stream.objects.all()
		resource_name = 'stream'
		filtering = {
			'created': ['exact', 'lt', 'lte', 'gte', 'gt'],
			'modified': ['exact', 'lt', 'lte', 'gte', 'gt'],
		}
	materials = fields.ToManyField(MaterialStatusResource, 'materials', full=True)
	authentication = SessionAuthentication()

	def dehydrate(self, bundle):
		bundle.data['tags'] = bundle.obj.tags.list()
		return bundle


class ProcessResource(PolymorphicModelResource):
	class Meta(object):
		queryset = Process.objects.all()
		resource_name = 'process'
		filtering = {
			'name': ['exact'],
		}
		authentication = SessionAuthentication()

	def dehydrate(self, bundle):
		super(ProcessResource, self).dehydrate(bundle)
		if hasattr(bundle.obj, 'get_ordered_subprocesses'):
			subprocesses = [ {'id': p.id, 'class': p.__class__.__name__, 'name': p.name} for p in bundle.obj.get_ordered_subprocesses() ]
			self.extend_key(bundle.data, self.get_class_name(bundle), { 'processes' : subprocesses })
		return bundle