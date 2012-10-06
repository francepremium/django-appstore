import unittest
from mock import call
from mock_django.signals import mock_signal_receiver

from signals import post_app_install, post_app_uninstall
from models import App, AppCategory, AppVersion, Environment


class BackendTestCase(unittest.TestCase):
    def tearDown(self):
        Environment.objects.all().delete()
        App.objects.all().delete()
        AppCategory.objects.all().delete()
        AppVersion.objects.all().delete()

    def test_001_simple_app(self):
        app = App.objects.create(name='artists',
            category=AppCategory.objects.create(name='art'))
        appversion = AppVersion.objects.create(app=app, version=0)
        env = Environment.objects.create(name='default')

        with mock_signal_receiver(post_app_install) as install_receiver:
            env.install(appversion)
            self.assertEqual(install_receiver.call_args_list, [
                call(signal=post_app_install, sender=env,
                    appversion=appversion),
            ])

        self.assertEqual(list(env.appversions.all()), [appversion])
        self.assertIn(app, env.installed_apps)

        with mock_signal_receiver(post_app_uninstall) as uninstall_receiver:
            env.uninstall(appversion)
            self.assertEqual(uninstall_receiver.call_args_list, [
                call(signal=post_app_uninstall, sender=env,
                    appversion=appversion),
            ])

        self.assertEqual(list(env.appversions.all()), [])
        self.assertEqual(0, len(env.installed_apps))

    def test_002_simple_dependency(self):
        artists_app = App.objects.create(name='artists',
            category=AppCategory.objects.create(name='art'))
        artists_appversion = AppVersion.objects.create(app=artists_app, version=0)

        artworks_app = App.objects.create(name='artworks',
            category=AppCategory.objects.get(name='art'))
        artworks_appversion = AppVersion.objects.create(app=artworks_app, version=0)
        artworks_appversion.dependencies.add(artists_appversion)

        env = Environment.objects.create(name='default')

        with mock_signal_receiver(post_app_install) as install_receiver:
            env.install(artworks_appversion)
            self.assertEqual(install_receiver.call_args_list, [
                call(signal=post_app_install, sender=env,
                    appversion=artists_appversion),
                call(signal=post_app_install, sender=env,
                    appversion=artworks_appversion),
            ])
