from django.conf.urls import patterns, include, url
from tastypie.api import Api
from factopy.api import StreamResource, MaterialResource, MaterialStatusResource, ProcessResource


api_v1 = Api(api_name='v1')
api_v1.register(StreamResource())
api_v1.register(MaterialResource())
api_v1.register(MaterialStatusResource())
api_v1.register(ProcessResource())

urlpatterns = patterns('',
    url(r'^api/', include(api_v1.urls)),
    url(r'^program/$', 'factopy.views.index'),
    url(r'^program/execute/(?P<program_id>\d+)/$', 'factopy.views.execute'),
    url(r'^program/status$', 'factopy.views.status'),
    url(r'^program/update$', 'factopy.views.update'),
)