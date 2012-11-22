import unittest
from mock import call
from mock_django.signals import mock_signal_receiver

from ..exceptions import (AppAlreadyInstalled, AppNotInstalled,
    CannotUninstallDependency, UpdateAlreadyPendingDeployment)
from ..signals import post_app_install, post_app_uninstall, post_app_copy
from ..models import App, AppCategory, AppFeature, Environment


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.instrument_feature = AppFeature.objects.create(name='instrument')

        self.ukulele_app = App.objects.create(name='ukulele', deployed=True,
            provides=self.instrument_feature, default_for_feature=True)
        self.piano_app = App.objects.create(name='piano', deployed=True,
            provides=self.instrument_feature)
        self.music_app = App.objects.create(name='music', deployed=True)
        self.music_app.requires.add(self.instrument_feature)

        self.env = Environment.objects.create(name='default')

    def tearDown(self):
        App.objects.all().delete()
        AppCategory.objects.all().delete()
        AppFeature.objects.all().delete()
        Environment.objects.all().delete()

    def test_mark_dirty(self):
        app = App(name='foo', superseeds=self.ukulele_app)
        app.save()

        self.assertFalse(hasattr(app, '_updating'))

        app.deployed = True
        app.save()

        self.assertTrue(app._updating)

    def test_raises_AppNotInstalled(self):
        with self.assertRaises(AppNotInstalled) as cm:
            self.env.uninstall(self.ukulele_app)

    def test_simple_post_app_install_signal(self):
        with mock_signal_receiver(post_app_install) as install_receiver:
            self.env.install(self.ukulele_app)

            self.assertEqual(install_receiver.call_args_list, [
                call(signal=post_app_install, sender=self.env,
                    app=self.ukulele_app),
            ])

    def test_simple_install(self):
        self.env.install(self.ukulele_app)
        self.assertEqual(list(self.env.apps.all()), [self.ukulele_app])

    def test_raises_AppAlreadyInstalled(self):
        self.env.install(self.ukulele_app)
        with self.assertRaises(AppAlreadyInstalled) as cm:
            self.env.install(self.ukulele_app)

    def test_simple_post_app_uninstall_signal(self):
        self.env.install(self.ukulele_app)

        with mock_signal_receiver(post_app_uninstall) as uninstall_receiver:
            self.env.uninstall(self.ukulele_app)

            self.assertEqual(uninstall_receiver.call_args_list, [
                call(signal=post_app_uninstall, sender=self.env,
                    app=self.ukulele_app),
            ])

    def test_simple_uninstall(self):
        self.env.install(self.ukulele_app)
        self.env.uninstall(self.ukulele_app)
        self.assertEqual(list(self.env.apps.all()), [])

    def test_install_dependency(self):
        with mock_signal_receiver(post_app_install) as install_receiver:
            self.env.install(self.music_app)
            self.assertEqual(install_receiver.call_args_list, [
                call(signal=post_app_install, sender=self.env,
                    app=self.ukulele_app),
                call(signal=post_app_install, sender=self.env,
                    app=self.music_app),
            ])

    def test_raises_CannotUninstallDependency(self):
        self.env.install(self.music_app)

        with self.assertRaises(CannotUninstallDependency) as cm:
            self.env.uninstall(self.ukulele_app)

    def test_uninstall_dependency(self):
        self.env.install(self.ukulele_app)
        self.env.install(self.piano_app)
        self.env.install(self.music_app)
        self.env.uninstall(self.ukulele_app)
        self.assertEqual([self.music_app, self.piano_app], list(self.env.apps.all()))

    def test_dont_install_dependency(self):
        self.env.install(self.piano_app)
        self.env.install(self.music_app)
        self.assertEqual([self.music_app, self.piano_app], list(self.env.apps.all()))

    def test_post_app_edit_signal(self):
        self.env.install(self.music_app)

        with mock_signal_receiver(post_app_copy) as edit_receiver:
            new_app = self.env.copy(self.ukulele_app)

            self.assertEqual(edit_receiver.call_args_list, [
                call(signal=post_app_copy, sender=self.env,
                    source_app=self.ukulele_app, new_app=new_app),
            ])

    def test_copy(self):
        self.env.install(self.music_app)

        new_app = self.env.copy(self.ukulele_app)

        self.assertEqual(self.ukulele_app.name, new_app.name)
        self.assertEqual(self.ukulele_app.description, new_app.description)
        self.assertEqual(self.ukulele_app.image, new_app.image)
        self.assertEqual(self.ukulele_app.category, new_app.category)
        self.assertEqual(self.ukulele_app.provides, new_app.provides)
        self.assertEqual(self.ukulele_app.editor, new_app.editor)
        self.assertEqual(None, new_app.superseeds_id)

        self.assertEqual([self.music_app, self.ukulele_app, new_app], list(self.env.apps.all()))

    def test_copy_superseed(self):
        self.env.install(self.music_app)

        new_app = self.env.copy(self.ukulele_app, superseed=True)

        self.assertEqual(self.ukulele_app, new_app.superseeds)

    def test_update_deploy(self):
        self.env.install(self.music_app)
        new_app = self.env.copy(self.ukulele_app, True)

        new_app.name = 'Fork'
        new_app.deployed = True
        new_app.save()

        self.assertEqual([new_app, self.music_app], list(self.env.apps.all()))

    def test_raises_UpdateAlreadyPendingDeployment(self):
        self.env.install(self.music_app)
        new_app = self.env.copy(self.ukulele_app, True)

        with self.assertRaises(UpdateAlreadyPendingDeployment) as cm:
            self.env.copy(self.ukulele_app, True)
