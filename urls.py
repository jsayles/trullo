from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
	(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.gif'}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

	(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
	(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),

	(r'^publish/', include('trullo.publish.urls')),
	(r'^', include('trullo.front.urls')),
)

if settings.DEBUG:
	urlpatterns += staticfiles_urlpatterns()

	urlpatterns += patterns('',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
			'document_root': settings.MEDIA_ROOT,
		}),
	)
