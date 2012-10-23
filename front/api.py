from tastypie.api import Api
from tastypie import fields, utils
from tastypie.paginator import Paginator
from datetime import datetime, timedelta, date
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect

from models import UserProfile

from trullo import API

class UserProfileResource(ModelResource):
	class Meta:
		queryset = UserProfile.objects.all()
		allowed_methods = ['get']
API.register(UserProfileResource())


class UserResource(ModelResource):
	profile = fields.ToOneField(UserProfileResource, 'profile', full=True)

	class Meta:
		queryset = User.objects.all()
		allowed_methods = ['get']
		fields = ['username', 'first_name', 'last_name', 'is_staff']
		filtering = { "is_staff": ('exact',) }
API.register(UserResource())
