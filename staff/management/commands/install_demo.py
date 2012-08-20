import os
import sys
import time
import urllib
import random
from datetime import datetime, date, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from publish.models import Log, Publication, Idea, Project, Comment, Link

class Command(BaseCommand):
	help = "Installs the demo data."
	requires_model_validation = True
	
	def handle(self, *labels, **options):
		if settings.PRODUCTION:
			print 'I will not install the demo on a PRODUCTION machine.  Sorry.'
			return

		call_command('syncdb', interactive=False)
		call_command('migrate', interactive=False)

		for log in Log.objects.all(): log.delete()
		for publication in Publication.objects.all(): publication.delete()
		for idea in Idea.objects.all(): idea.delete()
		for project in Project.objects.all(): project.delete()
		for comment in Comment.objects.all(): comment.delete()
		for link in Link.objects.all(): link.delete()

		site = Site.objects.get_current()
		site.domain = '127.0.0.1:8000'
		site.name = 'Dinker McDink'
		site.save()

		user1 = self.create_user('alice', '1234', 'Alice', 'Smith', is_staff=True, is_superuser=True)
		user2 = self.create_user('bob', '1234', 'Bob', 'Jones', is_staff=False, is_superuser=False)



	def create_user(self, username, password, first_name=None, last_name=None, is_staff=False, is_superuser=False):
		user, created = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name, is_staff=is_staff, is_superuser=is_superuser)
		user.set_password(password)
		user.save()
		return user
