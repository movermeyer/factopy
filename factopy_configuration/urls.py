from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

# Api provide an easy way of automatically determining the URL conf.

admin.autodiscover()

urlpatterns = \
    patterns('',
             url(r'^factopy/', include('factopy.urls')),
             url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
             url(r'^admin/', include(admin.site.urls)),
             )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),)
