from django.contrib import admin
from django import forms
from django.forms.util import ErrorList

from models import *

class StyledAdmin(admin.ModelAdmin):
	class Media:
		css = { "all": ('front/css/admin.css', )}

class CommentAdmin(StyledAdmin):
	list_display = ('author', 'created', 'censored')
admin.site.register(Comment, CommentAdmin)

class ProjectAdmin(StyledAdmin):
	list_display = ('title', 'started', 'ended', 'public', 'portfolio')
admin.site.register(Project, ProjectAdmin)

class IdeaAdmin(StyledAdmin):
	list_display = ('title', 'created')
	search_fields = ('title', 'description')
admin.site.register(Idea, IdeaAdmin)

class PhotoAdmin(StyledAdmin):
	pass
admin.site.register(Photo, PhotoAdmin)

class PublicationAdmin(StyledAdmin):
	list_display = ('title', 'venue', 'publication_date')
admin.site.register(Publication, PublicationAdmin)

class LogAdmin(StyledAdmin):
	pass
admin.site.register(Log, LogAdmin)

class LogEntryPhotoInline(admin.TabularInline):
	raw_id_fields = ('photo', )
	model = LogEntryPhoto
	extra = 2

class LogEntryAdmin(StyledAdmin):
	list_display = ('__unicode__', 'log', 'created', 'publish')
	inlines = (LogEntryPhotoInline,)
	date_hierarchy = 'created'
	search_fields = ('subject', 'content')
admin.site.register(LogEntry, LogEntryAdmin)

class LogEntryPhotoAdmin(StyledAdmin):
	pass
admin.site.register(LogEntryPhoto, LogEntryPhotoAdmin)

class LogFeedAdmin(StyledAdmin):
	pass
admin.site.register(LogFeed, LogFeedAdmin)

class LinkAdmin(StyledAdmin):
	pass
admin.site.register(Link, LinkAdmin)
