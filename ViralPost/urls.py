from django.conf.urls import patterns, include, url
from contacts.views import home, google_login, contact, google_authenticate, print_contact

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ViralPost.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$',home),
    url(r'^oauth/$',google_login),
    url(r'^callback/$',contact),
    url(r'^contacts/$',print_contact)
)
