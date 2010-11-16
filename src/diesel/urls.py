from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from diesel import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^fuel/$', 'fuel.views.index'),
    (r'^fuel/login$', 'fuel.views.diesellogin'),
    (r'^fuel/logout$', 'fuel.views.diesellogout'),
    (r'^fuel/announcement/add$', 'fuel.views.addAnnouncement'),
    (r'^accounts/', include('registration.backends.default.urls')),             
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )


