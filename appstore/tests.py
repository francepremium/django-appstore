import unittest
from mock import call
from mock_django.signals import mock_signal_receiver

from django.contrib.auth.models import User

from exceptions import AppAlreadyInstalled, AppVersionNotInstalled, CannotUninstallDependency
from signals import post_app_install, post_app_uninstall
from models import App, AppCategory, AppVersion, Environment


class BackendTestCase(unittest.TestCase):
    def setUp(self):
        self.user, c = User.objects.get_or_create(username='foo')
        self.appcategory = AppCategory.objects.create(name='art')

        self.artists_app = App.objects.create(name='artists',
            category=self.appcategory)
        self.artists_appversion = AppVersion.objects.create(
            app=self.artists_app, version=0, author=self.user, public=True)

        self.artworks_app = App.objects.create(name='artworks',
            category=self.appcategory)
        self.artworks_appversion = AppVersion.objects.create(
            app=self.artworks_app, version=0, author=self.user, public=True)
        self.artworks_appversion.dependencies.add(self.artists_app)

        self.env = Environment.objects.create(name='default')

    def tearDown(self):
        Environment.objects.all().delete()
        App.objects.all().delete()
        AppCategory.objects.all().delete()
        AppVersion.objects.all().delete()

    def test_001_simple_app(self):
        with self.assertRaises(AppVersionNotInstalled) as cm:
            self.env.uninstall_appversion(self.artists_appversion)

        with mock_signal_receiver(post_app_install) as install_receiver:
            self.env.install_appversion(self.artists_appversion)
            self.assertEqual(install_receiver.call_args_list, [
                call(signal=post_app_install, sender=self.env,
                    appversion=self.artists_appversion),
            ])

        self.assertEqual(list(self.env.appversions.all()),
                [self.artists_appversion])
        self.assertEqual([self.artists_app], list(self.env.installed_apps))

        with mock_signal_receiver(post_app_uninstall) as uninstall_receiver:
            self.env.uninstall_appversion(self.artists_appversion)
            self.assertEqual(uninstall_receiver.call_args_list, [
                call(signal=post_app_uninstall, sender=self.env,
                    appversion=self.artists_appversion),
            ])

        self.assertEqual(list(self.env.appversions.all()), [])
        self.assertEqual(0, len(self.env.installed_apps))

    def test_002_simple_dependency(self):
        with mock_signal_receiver(post_app_install) as install_receiver:
            self.env.install_appversion(self.artworks_appversion)
            self.assertEqual(install_receiver.call_args_list, [
                call(signal=post_app_install, sender=self.env,
                    appversion=self.artists_appversion),
                call(signal=post_app_install, sender=self.env,
                    appversion=self.artworks_appversion),
            ])

        self.assertEqual([self.artists_appversion, self.artworks_appversion],
            list(self.env.appversions.all()))

        with self.assertRaises(AppAlreadyInstalled) as cm:
            self.env.install_appversion(self.artists_appversion)

        with self.assertRaises(CannotUninstallDependency) as cm:
            self.env.uninstall_appversion(self.artists_appversion)

        with mock_signal_receiver(post_app_uninstall) as uninstall_receiver:
            self.env.uninstall_appversion(self.artworks_appversion)
            self.assertEqual(uninstall_receiver.call_args_list, [
                call(signal=post_app_uninstall, sender=self.env,
                    appversion=self.artworks_appversion),
            ])

        self.assertEqual([self.artists_appversion],
            list(self.env.appversions.all()))

    def test_003_fork(self):
        forker = User.objects.create(username='test_003_fork')
        fork = self.artworks_appversion.fork(forker)

        self.assertEqual(fork.version, self.artworks_appversion.version)
        self.assertEqual(fork.app, self.artworks_app)
        self.assertFalse(fork.public)
        self.assertEqual(fork.author, forker)
        self.assertListEqual(list(fork.dependencies.all()), [self.artists_app])
