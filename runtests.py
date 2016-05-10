import os
import sys

try:
    from django.conf import settings
    from django.test.utils import get_runner

    TEST_ROOT = os.path.dirname(__name__)

    settings.configure(
        DEBUG=False,
        TEMPLATE_DEBUG=False,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="tests.urls",
        LANGUAGE_CODE='en',
        LANGUAGES=(
            ('en', 'English'),
        ),
        CMS_LANGUAGES={
            1: [
                {
                    'code': 'en',
                    'name': 'English',
                    'public': True,
                },
            ],
            'default': {
                'hide_untranslated': False,
            },
        },
        CMS_TEMPLATES=(
            ('meta_tagger/index.html', 'Index'),
        ),
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            'django.contrib.admin',
            "cms",
            "menus",
            "treebeard",
            "easy_thumbnails",
            "filer",
            "meta_tagger",
            "tests.sample_app",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': ['tests/templates'],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.template.context_processors.tz',
                        'django.core.context_processors.request',
                        'django.contrib.messages.context_processors.messages',
                        'cms.context_processors.cms_settings',
                    ],
                },
            },
        ],
        STATIC_URL='/static/'
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
