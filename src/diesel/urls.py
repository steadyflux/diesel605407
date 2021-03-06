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
    
    (r'^fuel/user/profile', 'fuel.views.userProfile'),
    (r'^fuel/user/update', 'fuel.views.userUpdate'),
    (r'^fuel/user/delete', 'fuel.views.userDelete'),
    
    (r'^fuel/station/search/$', 'fuel.views.searchScreen'),
    (r'^fuel/station/search/load', 'fuel.views.searchScreen'),
    (r'^fuel/station/search/perform', 'fuel.views.searchPerform'),
    
    (r'^fuel/station/(?P<id>\d+)', 'fuel.views.stationHome'),
    (r'^fuel/station/image/(?P<id>\d+)', 'fuel.views.uploadStationImage'),
    (r'^fuel/station/price/(?P<id>\d+)', 'fuel.views.priceUpdate'),
    (r'^fuel/station/comment/(?P<id>\d+)', 'fuel.views.addStationComment'),
    
    (r'^accounts/', include('registration.backends.default.urls')),             
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )


