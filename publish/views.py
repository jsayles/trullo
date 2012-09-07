import rfc822
import tweepy
import urllib
import calendar
import traceback
from datetime import datetime, timedelta, date

from django.db.models import Q
from django.contrib import auth
from django.conf import settings
from django.core.cache import cache
from django.utils.html import urlize
from django.utils import feedgenerator
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template import Context, loader
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import django.contrib.contenttypes.models as content_type_models
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.admin.views.decorators import staff_member_required

from forms import CollectForm, LinkForm, IdeaForm, CommentForm
from models import Photo, Publication, Idea, Project, Comment, Log, LogEntry, ImageEntry, LogEntryPhoto, LogFeed, Link

def index(request):
	return render_to_response('publish/index.html', { 'logs':Log.objects.all() }, context_instance=RequestContext(request))

def update_twitter(request):
	log = get_object_or_404(Log, slug=settings.TWITTER_LOG_SLUG)
	twitter_auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
	twitter_auth.set_access_token(settings.TWITTER_ACCESS_KEY, settings.TWITTER_ACCESS_SECRET)
	twitter_api = tweepy.API(twitter_auth)
	for status in twitter_api.user_timeline():
		print status.id
		if LogEntry.objects.filter(log=log, source_guid=str(status.id)).count() == 0:
			entry = LogEntry(log=log)
			entry.content = urlize(status.text)
			entry.issued = status.created_at
			entry.source_date = status.created_at
			entry.source_guid = status.id
			entry.source_url = 'http://twitter.com/%s/status/%s' % (settings.TWITTER_USERNAME, status.id)
			entry.publish = True
			entry.save()
	return HttpResponse('Ok')

def check_log_feeds(request):
	for log_feed in LogFeed.objects.all():
		try:
			log_feed.check_feed()
		except:
			logging.exception("Error in reader import")
	return render_to_response('publish/check_log_feeds.html', { }, context_instance=RequestContext(request))

def publications(request):
	return render_to_response('publish/publications.html', { 'publications':Publication.objects.all() }, context_instance=RequestContext(request))

def merge(request):
	if request.user.is_staff:
		entries = LogEntry.objects.all()
	else:
		entries = LogEntry.objects.public_entries()
	return render_to_response('publish/merge/splash.html', { 'entries':entries }, context_instance=RequestContext(request))

def ideas(request):
	return render_to_response('publish/ideas.html', { 'ideas':Idea.objects.all() }, context_instance=RequestContext(request))

@login_required
def collect(request):
	return render_to_response('publish/collect.html', { }, context_instance=RequestContext(request))

@login_required
def collect_popup(request):
	page_message = None
	if request.method == 'GET':
		collect_form = CollectForm()
		if request.GET.has_key('url'): collect_form.initial['url'] = request.GET['url']
		if request.GET.has_key('title'): collect_form.initial['title'] = request.GET['title']
		if request.GET.has_key('excerpt') and len(request.GET['excerpt']) > 0:
			collect_form.initial['excerpt'] = request.GET['excerpt']
		elif request.GET.has_key('md'):
			collect_form.initial['excerpt'] = request.GET['md']
	else:
		collect_form = CollectForm(request.POST)
		if collect_form.is_valid():
			log_entry = LogEntry()
			log_entry.log = collect_form.cleaned_data['log']
			log_entry.subject = collect_form.cleaned_data['title']
			log_entry.content = '<blockquote>%s</blockquote><p class="collection-note">%s</p>' % (collect_form.cleaned_data['excerpt'] or '', collect_form.cleaned_data['note'] or '')
			log_entry.publish = collect_form.cleaned_data['make_public']
			log_entry.source_url = collect_form.cleaned_data['url']
			log_entry.issued = datetime.now()
			log_entry.save()
			page_message = 'The <a href="%s">log entry</a> was created.' % reverse('trullo.publish.views.log_entry_detail', args=[], kwargs={'slug':log_entry.log.slug, 'pk':log_entry.id})
	return render_to_response('publish/popup/collect.html', { 'collect_form':collect_form, 'page_message':page_message }, context_instance=RequestContext(request))


@login_required
def mobile_index(request): return render_to_response('publish/mobile/index.html', { }, context_instance=RequestContext(request))

@login_required
def mobile_ideas(request):
	message = None
	if request.method == 'POST' and request.user.is_staff:
		idea_form = IdeaForm(request.POST)
		if idea_form.is_valid():
			idea_form.save()
			idea_form = IdeaForm()
			message = 'Your idea was added.'
	else:
		idea_form = IdeaForm()
	print message
	return render_to_response('publish/mobile/ideas.html', { 'message':message, 'idea_form':idea_form, 'ideas':Idea.objects.all().order_by('title') }, context_instance=RequestContext(request))

@login_required
def mobile_idea(request, id):
	idea = get_object_or_404(Idea, pk=id)
	message = None
	if request.method == 'POST' and request.user.is_staff:
		idea_form = IdeaForm(request.POST, instance=idea)
		if idea_form.is_valid():
			idea_form.save()
			idea_form = IdeaForm(instance=idea)
			message = 'Your idea was added.'
	else:
		idea_form = IdeaForm(instance=idea)
	print message
	return render_to_response('publish/mobile/idea.html', { 'message':message, 'idea_form':idea_form, 'idea':idea }, context_instance=RequestContext(request))
		
def projects(request):
	return render_to_response('publish/projects.html', { 'projects':Project.objects.all() }, context_instance=RequestContext(request))

def links(request):
	return render_to_response('publish/links.html', { 'links':Link.objects.all() }, context_instance=RequestContext(request))

def image_detail(request, id):
	return render_to_response('publish/image_detail.html', {}, context_instance=RequestContext(request))
	
def stream_detail(request, slug):
	log = get_object_or_404(Log, slug=slug)
	if not request.user.is_staff and not log.public:
		return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
	return render_to_response('publish/%s/splash.html' % log.template, { 'log':log, 'archive_years':LogEntry.objects.filter(log=log).dates("issued", "year") }, context_instance=RequestContext(request))

def stream_archive(request, slug):
	return stream_year_archive(request, slug, datetime.now().year)

def stream_year_archive(request, slug, year):
	log = get_object_or_404(Log, slug=slug)
	if not request.user.is_staff and not log.public:
		return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
	return render_to_response('publish/%s/archive.html' % log.template, { 'log':log, 'entries':LogEntry.objects.filter(log=log, issued__year=year),'archive_years':LogEntry.objects.filter(log=log).dates("issued", "year") }, context_instance=RequestContext(request))

def stream_feed(request, slug):
	log = get_object_or_404(Log, slug=slug)
	if not request.user.is_staff and not log.public:
		return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)

	cache_key = "trullo.feed.stream.%s" % slug
	cached_feed = cache.get(cache_key)
	if cached_feed: return HttpResponse(cached_feed, mimetype='application/rss+xml')
	
	site = Site.objects.get_current()
	feed = feedgenerator.DefaultFeed(
		title = log.title,
		link = "http://" + site.domain + log.get_absolute_url(),
		feed_url = "http://" + site.domain + log.get_feed_url(),
		description=log.tagline,
		language="en",
	)
	for entry in log.published_entries().all()[:10]: add_log_entry_to_feed(entry, feed)
	cached_feed = feed.writeString('utf-8')
	cache.set(cache_key, cached_feed, 360)
	return HttpResponse(cached_feed, mimetype='application/rss+xml')

def add_log_entry_to_feed(entry, feed):
	if entry.source_url:
		link = entry.get_absolute_url()
	else:
		link = "http://%s%s" % (Site.objects.get_current().domain, entry.get_absolute_url())
	feed.add_item(title=strip_tags(entry.subject), link=link, description=entry.content, pubdate=entry.issued)

def add_story_to_feed(story, feed):
	site = Site.objects.get_current()
	if story.authors.all().count() > 0:
		author_name = story.authors.all()[0].get_profile().display_name
	else:
		author_name = None
	link = "http://" + site.domain + story.get_absolute_url()
	feed.add_item(title=strip_tags(story.headline), link=link, description=story.body, author_name=author_name, pubdate=story.start_date)

def log_entry_detail(request, slug, pk):
	entry = get_object_or_404(LogEntry, log__slug=slug, pk=pk)
	if not request.user.is_staff:
		if not entry.publish: raise Http404
		if not entry.log.public: raise Http404
	
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
	else:
		comment_form = CommentForm()
	if comment_form.is_valid() and entry.comments_open:
		if validate_form_keypair(request.POST.get('form_key', None), request.POST.get('form_value', None)):
			comment = Comment(author=comment_form.cleaned_data['author'], email=comment_form.cleaned_data['email'], url=comment_form.cleaned_data['url'])
			comment.created = datetime.now()
			comment.content_object = entry
			comment.comment = strip_tags(comment_form.cleaned_data['comment'])
			comment.ip = request.META['REMOTE_ADDR']
			comment.save()
		else:
			logging.info('received an unvalidated form from %s: %s' % (request.META['REMOTE_ADDR'], comment_form.POST.get('author', None)))
	form_key, form_value = generate_form_keypair()
	return render_to_response('publish/%s/entry.html' % entry.log.template, { 'entry':entry, 'log':entry.log, 'comment_form':comment_form, 'form_key':form_key, 'form_value':form_value, 'archive_years':LogEntry.objects.filter(log=entry.log).dates("issued", "year") }, context_instance=RequestContext(request))

def generate_form_keypair():
	"""Used by forms which want to doublecheck that they're not robotic entries.  Returns a unique but validatable key/value pair to be used in a hidden form element."""
	return (str(time.time()), str(time.time()))

def validate_form_keypair(key, value):
	print 'validating: %s %s' % (key, value)
	try:
		timeout_minutes = 15
		key_time = datetime.utcfromtimestamp(float(key))
		value_time = datetime.utcfromtimestamp(float(value))
		if key_time > datetime.utcnow(): return False
		if key_time < datetime.utcnow() - timedelta(minutes=timeout_minutes): return False
		if value_time > datetime.utcnow(): return False
		if value_time < datetime.utcnow() - timedelta(minutes=timeout_minutes): return False
	except:
		traceback.print_exc()
		return False
	return True

# Copyright 2012 Trevor F. Smith (http://trevor.smith.name/) 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
