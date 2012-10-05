django-appstore
===============

Status: beta software.

Features
--------

This app intends to provide a simple appstore for django. It is inspired by
both Chrome App Store and uses the concept of Environment like Python's
brilliant ``PyPi`` and ``virtualenv``.

It is left to the user of this app to connect post_app_install and
post_app_uninstall, because this app is just a helper to make your own app
system.

Templates and staticfiles use twitter bootstrap.

Install
-------

- install sources from github with ``pip install -e git+....``,
- install models by adding ``appstore`` to ``INSTALLED_APPS`` and run
  ``syncdb`` or ``migrate``,
- include urls by adding ``url(r'appstore/', include('appstore.urls'))`` to
  ``urls.py``,
- install templates by overriding ``appstore/base.html`` to customize the
  parent template and blocks.
- if you have problems with static files, rely on Django's documentation or
  YourLabs blog article which is shorter,
- implement ``post_app_install`` and ``post_app_uninstall`` signals like you
  want.

Documentation / design
----------------------

Views & urls
````````````

appstore_app_list
    Use AppListView, a filterable list of Apps.

appstore_app_details
    Used as modal.

appstore_app_action
    Performs an action on an environment, action can be 'install' or
    'uninstall'.

Models
``````

- App model represents an app,
- AppCategory model allows to sort App by category in AppCategoryView,
- AppVersion model represents a version of an App, contains dependency info,
- Environment model keeps track of installed apps and versions,

App and AppCategory are dumb models used to build a catchy Chrome App
Store-like frontend. AppVersion and Environment are used to build the Pythonic
package management backend.

Signals
```````

post_app_install
    Triggered when an app is installed into an environment.

post_app_uninstall
    Triggered when an app is uninstalled from an environment.
