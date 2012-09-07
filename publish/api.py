from tastypie.api import Api
from tastypie.resources import ModelResource
from datetime import datetime, timedelta, date

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect

from models import Project, Idea

class ProjectResource(ModelResource):
	class Meta:
		queryset = Project.objects.all()

	def get_object_list(self, request):
		projects = super(ProjectResource, self).get_object_list(request)
		if request.user.is_authenticated(): return projects
		return projects.filter(public=True)

	def prepend_urls(self):
		return [
			url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
		]

class IdeaResource(ModelResource):
	class Meta:
		queryset = Idea.objects.all()

V1_API = Api(api_name='v0.1')
V1_API.register(ProjectResource())
V1_API.register(IdeaResource())

urlpatterns = patterns('',
	(r'^', include(V1_API.urls)),
)

