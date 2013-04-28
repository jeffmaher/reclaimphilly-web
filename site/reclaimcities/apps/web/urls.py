from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'reclaimcities.apps.web.views.index'),
                       url(r'^map/?$', 'reclaimcities.apps.web.views.map'),
                       url(r'^blog/?$', 'reclaimcities.apps.web.views.blog'),
                       url(r'^about/?$', 'reclaimcities.apps.web.views.about'),
                       url(r'^resources/?$', 'reclaimcities.apps.web.views.resources'),
                       url(r'^help/?$', 'reclaimcities.apps.web.views.help'),
                       url(r'^add/location/?$', 'reclaimcities.apps.web.views.add_location'),
                       url(r'^update/location/(?P<id>\d+)/?$', 'reclaimcities.apps.web.views.update_location'),
                       url(r'^location/(?P<id>\d+)/?$', 'reclaimcities.apps.web.views.view_location'),

)
