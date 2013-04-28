from django.conf.urls import patterns, include, url
from django.contrib import admin
import reclaimcities.settings.settings as settings
import reclaimcities.apps.web.urls
import reclaimcities.apps.api.urls

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^services/', include(reclaimcities.apps.api.urls)),
                       url(r'^', include(reclaimcities.apps.web.urls)),
)
