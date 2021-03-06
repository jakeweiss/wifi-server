from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wifi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^server/', include('server.urls', namespace='server')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^$', include('home.urls'))
)
