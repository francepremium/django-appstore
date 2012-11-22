import unittest

from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User

from ..models import Environment, UserEnvironment
from ..middleware import EnvironmentMiddleware


class UserEnvironmentTestCase(unittest.TestCase):
    def setUp(self):
        User.objects.all().delete()
        Environment.objects.all().delete()

    def make_user(self, name):
        return User.objects.create(email=u'%s@example.com' % name,
            username=name)

    def make_request(self, user):
        request = RequestFactory().get(reverse('appstore_appcategory_list'))
        request.user = user
        request.session = {}
        EnvironmentMiddleware().process_request(request)
        return request.session['appstore_environment']

    def test_auto_create_environment(self):
        user = self.make_user('x')
        env = self.make_request(user)

        self.assertEqual(env.name, 'x@example.com')
        self.assertTrue(env.is_admin(user))

    def test_user_invited_environment(self):
        admin = self.make_user('x')
        env = self.make_request(admin)

        user = self.make_user('y')
        ue = UserEnvironment.objects.create(environment=env, user=user)
        self.assertTrue(ue.default)
        result = self.make_request(user)

        self.assertEqual(result.name, 'x@example.com',
            'User should be connected to the env it was invited to')

        self.assertEqual(Environment.objects.count(), 1,
            'User should not have caused creation of a new env')

        self.assertFalse(result.is_admin(user),
            'User should not be admin in the env it was invited in')
