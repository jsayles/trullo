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

# Copyright 2012 Trevor F. Smith (http://trevor.smith.name/) 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
