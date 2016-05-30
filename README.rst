===========
meta-tagger
===========
This package handles the meta tags of your django CMS project. Some global stuff like the page author and publisher can
be managed as setting variables. Other things are stored in a page extension. If you have your own Django models you
can even use a mixin to have everything you need for your meta tags.

Requirements
------------

- ``Django`` >= 1.5
- ``django-cms`` >= 3.0

Quickstart
----------

Install meta-tagger::

    pip install meta-tagger

Load all template tags of this package ::

    {% load meta_tagger_tags %}

Configure installed apps in your ``settings.py`` ::

    INSTALLED_APPS = (
        ...,
        'meta_tagger',
    )

Render the content of the title tag ::

    <title>{% render_title_tag %}</title>

Include all the other meta tags::

    {% include 'meta_tagger/meta_tags.html' %}

Migrate your database ::

    $ ./manage.py migrate meta_tagger


Add the sitemap to your project urls.py ::

    from meta_tagger.cms_sitemap import MetaTagRobotsSiteMap

    urlpatterns = [
        ...,
        url(r'^sitemap\.xml/$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': MetaTagRobotsSiteMap}})
    ]

Features
--------

* Django CMS page extension for the ``robots`` meta tag and the open graph image.
* Mixin for app models to inherit page specific fields (e.g. meta title, robots, etc.)
* Include template that renders all meta tags.


Model mixin
-----------
This package provides several mixins for the models of your own Django apps. The usage of
``MetaTagTitleDescriptionMixin``, ``OpenGraphMixin``, ``RobotsMixin`` is straightforward like
any other mixin. If your view has a context variable called ``object``, which is the default value for the class based
generic ``DetailView``, you don't need to consider anything. Otherwise just pass the object as context to your view.

Make sure you don't forget to implement your translation settings before you create your migrations.

You might want to use one of your own model fields as meta title. By overriding the corresponding method
(e.g. get_meta_title), it is very easy to provide another value.


Static settings
---------------

To populate the global meta tags with values, just add the following lines to your ``settings.py`` ::

    META_TAGGER_META_TAG_CONF = {
        'META_AUTHOR': 'My author',
        'META_PUBLISHER': 'My publisher',
        'META_COPYRIGHT': '2016',
        'META_COMPANY': 'My company',
        'META_SITE_NAME': 'My site name',
        'META_TYPE': 'website',
    }

    META_TAGGER_ROBOTS_DOMAIN_WHITELIST = ['www.example.com']


Dynamic settings
----------------

If you are looking for a solution to manage the global meta tags in the admin rather than the settings file, you might
take a look at the ``constance`` package. The installation is pretty easy::

    pip install "django-constance[database]"
    pip install django-picklefield

Configure installed apps in your ``settings.py`` ::

    INSTALLED_APPS = (
        ...,
        'constance',
        'constance.backends.database',
    )

    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
    CONSTANCE_DATABASE_CACHE_BACKEND = 'default'
    CONSTANCE_ADDITIONAL_FIELDS = {
        'short_text': ['django.forms.fields.CharField', {'widget': 'django.forms.fields.TextInput'}],
    }
    CONSTANCE_CONFIG = {
        'META_AUTHOR': ('', '<meta name="author" content="{META_AUTHOR}">', 'short_text'),
        'META_PUBLISHER': ('', '<meta name="publisher" content="{META_PUBLISHER}">', 'short_text'),
        'META_COPYRIGHT': ('', '<meta name="copyright" content="{META_COPYRIGHT}">', 'short_text'),
        'META_COMPANY': ('', '<meta name="company" content="{META_COMPANY}">', 'short_text'),
        'META_SITE_NAME': ('', '<meta name="site-name" content="{META_SITE_NAME}">', 'short_text'),
        'META_TYPE': ('website', '<meta property="og:type" content="{META_TYPE}">', 'short_text'),
        'META_OG_IMAGE_WIDTH': (1200, '<meta property="og:image:width" content="{META_OG_IMAGE_WIDTH}">', int),
        'META_OG_IMAGE_HEIGHT': (630, '<meta property="og:image:height" content="{META_OG_IMAGE_HEIGHT}">', int),
    }

    META_TAGGER_ROBOTS_DOMAIN_WHITELIST = ['www.example.com']

Please refer to the documentation of django constance for additional installation support (e.g. Redis)


ROBOTS INDEXING
---------------

To prevent indexing any unwanted domains, the content of the robots meta tag defaults to ``noindex, nofollow``. All
domains listed in the setting variable use the configuration of your model instance or CMS page::

    META_TAGGER_ROBOTS_DOMAIN_WHITELIST = ['www.example.com']


Running Tests
-------------
::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
