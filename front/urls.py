from django.conf import settings
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'trullo.front.views.index'),
)