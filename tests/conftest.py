# pylint: disable=C0111
import os
from datetime import timedelta

test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')

postgres_container_userland_port = 65432  # required for travis, so using it everywhere


def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'postgres',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'PORT': '54321',
                'HOST': '127.0.0.1',
            }
        },
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'rest_framework',
            'rest_framework_gis',
            'rest_framework.authtoken',
            'tests',

            'osmaxx.conversion_job',
            'osmaxx.countries',
            'osmaxx.clipping_area',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.SHA1PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
            'django.contrib.auth.hashers.BCryptPasswordHasher',
            'django.contrib.auth.hashers.MD5PasswordHasher',
            'django.contrib.auth.hashers.CryptPasswordHasher',
        ),
        RQ_QUEUES={
            'default': {
                'HOST': 'localhost',
                'PORT': 6379,
                'DB': 0,
                'PASSWORD': '',
                'DEFAULT_TIMEOUT': 3600,
            },
        },
        JWT_AUTH={
            'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
            'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
            'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
            'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
            'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',

            'JWT_ALGORITHM': 'HS256',
            'JWT_VERIFY': True,
            'JWT_VERIFY_EXPIRATION': True,
            'JWT_LEEWAY': 0,
            'JWT_EXPIRATION_DELTA': timedelta(seconds=300),
            'JWT_AUDIENCE': None,
            'JWT_ISSUER': None,

            'JWT_ALLOW_REFRESH': False,
            'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),

            'JWT_AUTH_HEADER_PREFIX': 'JWT',
        },
        OSMAXX_CONVERSION_SERVICE={
            'PBF_PLANET_FILE_PATH': os.path.join(test_data_dir, 'osm', 'monaco-latest.osm.pbf'),
            'COUNTRIES_POLYFILE_LOCATION': os.path.join(test_data_dir, 'polyfiles'),
        },

    )
