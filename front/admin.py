from django.contrib import admin
from django import forms
from django.forms.util import ErrorList

from models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user',)
admin.site.register(UserProfile, UserProfileAdmin)