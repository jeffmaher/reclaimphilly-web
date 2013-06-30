from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^geocode/(?P<streetAddress>[\w\s,.-]+)/?$',
                           'reclaimcities.apps.api.rest_services.geocode'),
                       url(r'^locations/?$', 'reclaimcities.apps.api.rest_services.get_locations_in_radius'),
                       url(r'^location/(?P<id>\d+)/?$',
                           'reclaimcities.apps.api.rest_services.get_location_by_id'),
                       url(r'^location/?$', 'reclaimcities.apps.api.rest_services.add_location'),
                       url(r'^location/(?P<id>\d+)/update/?$',
                           'reclaimcities.apps.api.rest_services.update_location'),
)
