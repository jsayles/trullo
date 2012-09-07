from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
	(r'^$', 'trullo.publish.views.index'),
	(r'^link/$', 'trullo.publish.views.links'),
	(r'^idea/$', 'trullo.publish.views.ideas'),
	(r'^publication/$', 'trullo.publish.views.publications'),
	(r'^project/$', 'trullo.publish.views.projects'),
	(r'^image/(?P<id>[\d]+)/$', 'trullo.publish.views.image_detail'),

	(r'^merge/$', 'publish.views.merge'),

	(r'^collect/$', 'publish.views.collect'),
	(r'^collect/popup/$', 'publish.views.collect_popup'),

	(r'^m/$', 'trullo.publish.views.mobile_index'),
	(r'^m/idea/$', 'trullo.publish.views.mobile_ideas'),
	(r'^m/idea/(?P<id>\d+)/$', 'trullo.publish.views.mobile_idea'),

	(r'^(?P<slug>[^/]+)/$', 'trullo.publish.views.stream_detail'),
	(r'^(?P<slug>[^/]+)/archive/$', 'trullo.publish.views.stream_archive'),
	(r'^(?P<slug>[^/]+)/archive/(?P<year>[\d]+)/$', 'trullo.publish.views.stream_year_archive'),
	(r'^(?P<slug>[^/]+)/feed/$', 'trullo.publish.views.stream_feed'),
	(r'^(?P<slug>[^/]+)/(?P<pk>[\d]+)/$', 'trullo.publish.views.log_entry_detail'),
)

# Copyright 2012 Trevor F. Smith (http://trevor.smith.name/) 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
