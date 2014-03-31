from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'reclaimcities.apps.web.views.index'),
                       url(r'^map/?$', 'reclaimcities.apps.web.views.map'),
                       url(r'^about/?$', 'reclaimcities.apps.web.views.about'),
                       url(r'^help/?$', 'reclaimcities.apps.web.views.help'),
                       url(r'^add/location/?$', 'reclaimcities.apps.web.views.add_location'),
                       url(r'^update/location/(?P<id>\d+)/?$', 'reclaimcities.apps.web.views.update_location'),
                       url(r'^location/(?P<id>\d+)/?$', 'reclaimcities.apps.web.views.view_location'),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,})

)
