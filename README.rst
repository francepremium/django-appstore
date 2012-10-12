django-appstore
===============

Status: beta software.

Features
--------

This app intends to provide a simple appstore for django. It is inspired by
both Chrome App Store and uses the concept of Environment like Python's
brilliant ``virtualenv``.

It is left to the user of this app to connect post_app_install and
post_app_uninstall, because this app is just a helper to make your own app
system. It is actually made for our specific needs so you might prefer to fork
it rather than to try to use it as-is.

Templates and staticfiles use twitter bootstrap and jQuery.

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

appstore_appcategory_list
    Use AppCategoryList.

appstore_appcategory_detail
    Use AppCategoryDetail.

appstore_app_details
    Used as modal to describe an app, also receives an action such as 'install'
    or 'uninstall' as post.


Models
``````

- App model represents an app,
- AppFeature has just a name, and represents a feature of an App in
  App.provides,
- AppCategory model allows to sort App by category in AppCategoryView,
- AppVersion model represents a version of an App, relates to AppFeature in
  AppVersion.requires,
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
