from django.conf.urls import patterns, url, include
# import django.views.static.serve
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    url(r'^accounts/', include('account.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': '/home/bier/html/static'}),
)
