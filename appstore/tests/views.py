import unittest
import os.path

from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User

from django_webtest import webtest


IMAGE_PATH = os.path.join(settings.PROJECT_ROOT,
    'static/bootstrap/img/glyphicons-halflings.png')


class UserAppTestCase(unittest.TestCase):
    def test_create_app(self):
        self.app.get()
