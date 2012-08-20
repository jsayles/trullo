from django import forms
from django.utils.html import strip_tags
from django.contrib.auth.models import User

from models import *

class CollectForm(forms.Form):
   log = forms.ModelChoiceField(queryset=Log.objects.all(), required=True)
   url = forms.URLField(required=True)
   title = forms.CharField(required=True)
   excerpt = forms.CharField(widget=forms.Textarea, required=False)
   note = forms.CharField(required=False)
   make_public = forms.BooleanField(required=False, initial=True)

class LinkForm(forms.ModelForm):
	class Meta:
		model = Link
		fields = ('url', 'name', 'description', 'public')

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('author', 'email', 'url', 'comment')

class IdeaForm(forms.ModelForm):
	class Meta:
		model = Idea
		fields = ('title', 'description')