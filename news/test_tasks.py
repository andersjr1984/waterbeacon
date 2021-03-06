from datetime import datetime, timedelta, timedelta
from django.conf import settings
from django.test import TestCase
from utils.log import log

import factory
from mock import (
    mock, patch

)

from annoying.functions import get_object_or_None

from news import tasks, models

# ./manage.py test news.test_tasks.TaskViews --settings=settings.dev
class TaskViews(TestCase):

    def setUp(self):
        location = models.location()
        location.city = "St. Louis"
        location.status = 'info'
        location.save()

    def test_twitter_crawler(self):
        # ./manage.py test news.test_tasks.TaskViews.test_twitter_crawler --settings=settings.dev
        tasks.TweetWaterAdvisoryReader()
