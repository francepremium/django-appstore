import unittest

from django.contrib.auth.models import User

from ..forms import make_appformclass, EnvironmentForm


class FormsTestCase(unittest.TestCase):
    def setUp(self):
        self.admin, c = User.objects.get_or_create(username='admin',
            is_staff=True)
        self.user, c = User.objects.get_or_create(username='user')

    def test_admin_make_appformclass(self):
        fc = make_appformclass(self.admin)
        f = fc()

        import ipdb; ipdb.set_trace()
