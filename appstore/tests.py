import unittest
from mock import call
from mock_django.signals import mock_signal_receiver

from django.contrib.auth.models import User

from exceptions import AppAlreadyInstalled, AppVersionNotInstalled, CannotUninstallDependency
from signals import post_app_install, post_app_uninstall
from models import App, AppCategory, AppFeature, AppVersion, Environment


class FrontendTestCase(unittest.TestCase):
    pass


class BackendTestCase(unittest.TestCase):
    def setUp(self):
        self.user, c = User.objects.get_or_create(username='foo')
        self.appcategory = AppCategory.objects.create(name='art')
        self.artist_appfeature = AppFeature.objects.create(name='artist')
        self.artwork_appfeature = AppFeature.objects.create(name='artwork')

        self.artists_app = App.objects.create(name='artists',
            category=self.appcategory, provides=self.artist_appfeature,
            default_for_feature=True)
        self.artists_appversion = AppVersion.objects.create(
            app=self.artists_app, version=0, author=self.user, public=True)

        self.artworks_app = App.objects.create(name='generic artworks',
            category=self.appcategory, provides=self.artwork_appfeature,
            default_for_feature=True)
        self.artworks_appversion = AppVersion.objects.create(
            app=self.artworks_app, version=0, author=self.user, public=True)
        self.artworks_appversion.requires.add(self.artist_appfeature)

        self.paintings_app = App.objects.create(name='paintings',
            category=self.appcategory, provides=self.artwork_appfeature)
        self.paintings_appversion = AppVersion.objects.create(
            app=self.paintings_app, version=0, author=self.user, public=True)
        self.paintings_appversion.requires.add(self.artist_appfeature)

        self.env = Environment.objects.create(name='default')

    def tearDown(self):
        Environment.objects.all().delete()
        App.objects.all().delete()
        AppCategory.objects.all().delete()
        AppVersion.objects.all().delete()
        AppFeature.objects.all().delete()

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
        self.assertEqual(list(self.env.appfeatures), [self.artist_appfeature])

        with mock_signal_receiver(post_app_uninstall) as uninstall_receiver:
            self.env.uninstall_appversion(self.artists_appversion)
            self.assertEqual(uninstall_receiver.call_args_list, [
                call(signal=post_app_uninstall, sender=self.env,
                    appversion=self.artists_appversion),
            ])

        self.assertEqual(list(self.env.appversions.all()), [])
        self.assertEqual(0, len(self.env.installed_apps))
        self.assertEqual(list(self.env.appfeatures), [])

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

        self.env.install_app(self.artworks_app)

    def test_003_complex_dependency(self):
        with mock_signal_receiver(post_app_install) as install_receiver:
            self.env.install_appversion(self.paintings_appversion)
            self.assertEqual(install_receiver.call_args_list, [
                call(signal=post_app_install, sender=self.env,
                    appversion=self.artists_appversion),
                call(signal=post_app_install, sender=self.env,
                    appversion=self.paintings_appversion),
            ])

        self.assertEqual([self.artists_appversion, self.paintings_appversion],
            list(self.env.appversions.all()))

        with self.assertRaises(AppAlreadyInstalled) as cm:
            self.env.install_app(self.paintings_app)

        with self.assertRaises(CannotUninstallDependency) as cm:
            self.env.uninstall_app(self.artists_app)

        with mock_signal_receiver(post_app_uninstall) as uninstall_receiver:
            self.env.uninstall_appversion(self.paintings_appversion)
            self.assertEqual(uninstall_receiver.call_args_list, [
                call(signal=post_app_uninstall, sender=self.env,
                    appversion=self.paintings_appversion),
            ])

        self.assertEqual([self.artists_appversion],
            list(self.env.appversions.all()))

        self.env.install_app(self.artworks_app)
        self.assertEqual([self.artists_appversion, self.artworks_appversion],
            list(self.env.appversions.all()))

        self.env.install_app(self.paintings_app)
        self.assertEqual([self.artists_appversion, self.artworks_appversion,
            self.paintings_appversion],
            list(self.env.appversions.all()))

    def test_004_fork(self):
        forker = User.objects.create(username='test_003_fork')
        fork = self.artworks_appversion.fork(forker)

        self.assertEqual(self.artworks_app.name, fork.app.name)
        self.assertEqual(self.artworks_app.category, fork.app.category)
        self.assertEqual(self.artworks_app.image, fork.app.image)
        self.assertEqual(self.artworks_app.provides, fork.app.provides)
        self.assertFalse(fork.app.default_for_feature)
        self.assertEqual(self.artworks_app, fork.app.fork_of)

        self.assertEqual(fork.version, self.artworks_appversion.version)
        self.assertNotEqual(fork.app, self.artworks_app)
        self.assertFalse(fork.public)
        self.assertEqual(fork.author, forker)
        self.assertListEqual(list(fork.requires.all()), [self.artist_appfeature])
