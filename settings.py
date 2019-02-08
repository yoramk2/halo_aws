#  settings for  project.

import os
from environs import Env
import json

print("start base")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('BASE_DIR : {}'.format(BASE_DIR))

env = Env()
THE_ENV=os.path.join(BASE_DIR,'env','.env')
env.read_env(path=THE_ENV)
print('The .env file has been loaded. env: '+str(THE_ENV))

ENV = env.str('FLASK_ENV', default='production')
DEBUG = ENV == 'development'
SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
SECRET_KEY = env.str('SECRET_KEY')
BCRYPT_LOG_ROUNDS = env.int('BCRYPT_LOG_ROUNDS', default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False
WEBPACK_MANIFEST_PATH = 'webpack/manifest.json'

LOC = "loc"
DEV = "dev"
TST = "tst"
PRD = "prd"
ENV_TYPE = LOC
os.environ["HALO_TYPE"] = ENV_TYPE

ENV_NAME = LOC  # env.str('ENV_NAME')
os.environ["HALO_STAGE"] = ENV_NAME  # done in settings json file

FUNC_NAME = env.str('FUNC_NAME', 'halo_flask')
os.environ['HALO_FUNC_NAME'] = FUNC_NAME  # done in settings json file
os.environ['HALO_APP_NAME'] = 'app'  #done in settings json file

SERVER_LOCAL = True
AWS_REGION = env.str('AWS_REGION')
DB_URL = env('DYNAMODB_LOCAL_URL','')
if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
    DB_URL = env('DYNAMODB_URL')
    SERVER_LOCAL = False

# SECURITY WARNING: keep the secret key used in production secret!
# Make this unique, and don't share it with anybody.
SECRET_KEY = env('SECRET_KEY')

###
# Given a version number MAJOR.MINOR.PATCH, increment the:
#
# MAJOR version when you make incompatible  changes,
# MINOR version when you add functionality in a backwards-compatible manner, and
# PATCH version when you make backwards-compatible bug fixes.
###

title = 'webfront'
author = 'Author'
copyright = 'Copyright 2017-2018 ' + author
major = '1'
minor = '1'
patch = '52'
version = major + '.' + minor + '.' + patch
# year.month.day.optional_revision  i.e 2016.05.03 for today
rev = 1
build = '2018.10.10.' + str(rev)
generate = '2018.10.13.19:06:07'
print("generate=" + generate)


def get_version():
    """
    Return package version as listed in  env file
    """
    return version + "/" + build + ' (' + ENV_NAME + ')'


VERSION = get_version()
print(VERSION)

APPEND_SLASH = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # env.bool('DEBUG', default=True)
print("DEBUG=" + str(DEBUG))

SERVER = env('SERVER_NAME')
HALO_HOST = None
ALLOWED_HOSTS = ['*','127.0.0.1',SERVER]

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DB_VER = env('DB_VER')
PAGE_SIZE = env.int('PAGE_SIZE', default=5)
#DATABASES = {
#   'default': env.db(),
#}

def get_cache():
  return {
      'default': env.cache()
    }

#CACHES = get_cache()

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LOCALE_CODE = 'en-US'
LANGUAGE_CODE = 'en'

LANGUAGES = (
    #('en', _('English')),
    #('nl', _('Dutch')),
    #('he', _('Hebrew')),
)

GET_LANGUAGE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'


PROJECT_APPS = (
    'api',
)

CORS_ORIGIN_ALLOW_ALL = True
#change to proper site in production
#HOME_DOMAIN = env('HOME_DOMAIN')#'amazon.com'
#CORS_ORIGIN_WHITELIST = (
#    HOME_DOMAIN,
#    'localhost:8000',
#    '127.0.0.1:9000'
#)

STATIC_URL = '/static1/'

STATIC_ROOT = os.path.join(BASE_DIR, "halo_flask/api/static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '%(asctime)s; %(filename)s:%(lineno)d',
            'datefmt': "%Y-%m-%d %H:%M:%S",
            'class': "pythonjsonlogger.jsonlogger.JsonFormatter",
        },
        'main_formatter_old': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
    #    'file': {
    #        'level': 'DEBUG',
    #        'class': 'logging.FileHandler',
    #        'filename': '/path/to/django/debug.log',
    #    },
        #    'console': {
        #        'level': 'ERROR',
        #        'filters': ['require_debug_false'],
        #        'class': 'logging.StreamHandler',
        #        'formatter': 'main_formatter',
        #    },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'console_debug_false': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': True,
        },
        'halo_flask.halo_flask.views': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_flask.halo_flask.apis': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_flask.halo_flask.events': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_flask.halo_flask.mixin': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_flask.halo_flask.models': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_flask.halo_flask.util': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
        'halo_flask.halo_flask.ssm': {
            'level': 'INFO',
            'handlers': ['console', 'console_debug_false', 'mail_admins']
        },
    },
}

USER_HEADERS = 'Mozilla/5.0'

MIXIN_HANDLER = 'loader1service.api.mixin.mixin_handler'

SERVICE_READ_TIMEOUT_IN_SC = 0.3  # in seconds = 300 ms

SERVICE_CONNECT_TIMEOUT_IN_SC = 0.3  # in seconds = 300 ms

RECOVER_TIMEOUT_IN_SC = 0.5  # in seconds = 500 ms

MINIMUM_SERVICE_TIMEOUT_IN_SC = 0.1  # in seconds = 100 ms

HTTP_MAX_RETRY = 4

THRIFT_MAX_RETRY = 4

HTTP_RETRY_SLEEP = 0.100  # in seconds = 100 ms

FRONT_WEB = False

FRONT_API = False

import uuid

INSTANCE_ID = uuid.uuid4().__str__()[0:4]

LOG_SAMPLE_RATE = 0.05  # 5%

ERR_MSG_CLASS = 'halo_flask.mixin_err_msg'

#######################################################################################3

import json

API_CONFIG = None
API_SETTINGS = ENV_NAME + '_api_settings.json'

file_dir = os.path.dirname(__file__)
file_path = os.path.join(file_dir, API_SETTINGS)
with open(file_path, 'r') as fi:
    API_CONFIG = json.load(fi)
    print("api_config:" + str(API_CONFIG))

file_dir = os.path.dirname(__file__)
file_path = os.path.join(file_dir, 'loc_settings.json')
with open(file_path, 'r') as fi:
    LOC_TABLE = json.load(fi)
    print("loc_settings:" + str(LOC_TABLE))

SSM_CONFIG = None
if ENV_NAME == LOC:
    # from halo_flask.ssm import get_config as get_config
    try:
        from halo_flask.halo_flask.ssm import get_config, set_param_config
    except:
        from halo_flask.ssm import get_config, set_param_config

    SSM_CONFIG = get_config(AWS_REGION)
    # set_param_config(AWS_REGION, 'DEBUG_LOG', '{"val":"false"}')
    # SSM_CONFIG.get_param("test")

SSM_APP_CONFIG = None
if ENV_NAME == LOC:

    # from halo_flask.ssm import get_config as get_config
    try:
        from halo_flask.halo_flask.ssm import get_app_config, set_app_param_config
    except:
        from halo_flask.ssm import get_app_config, set_app_param_config

    SSM_APP_CONFIG = get_app_config(AWS_REGION)

    # api_config:{'About': {'url': 'http://127.0.0.1:7000/about/', 'type': 'api'}, 'Task': {'url': 'http://127.0.0.1:7000/task/$upcid/', 'type': 'api'}, 'Curr': {'url': 'http://127.0.0.1:7000/curr/', 'type': 'api'}, 'Top': {'url': 'http://127.0.0.1:7000/top/', 'type': 'api'}, 'Rupc': {'url': 'http://127.0.0.1:7000/upc/$upcid/', 'type': 'api'}, 'Upc': {'url': 'http://127.0.0.1:7000/upc/$upcid/', 'type': 'api'}, 'Contact': {'url': 'http://127.0.0.1:7000/contact/', 'type': 'api'}, 'Fail': {'url': 'http://127.0.0.1:7000/fail/', 'type': 'api'}, 'Rtask': {'url': 'http://127.0.0.1:7000/task/$upcid/', 'type': 'api'}, 'Page': {'url': 'http://127.0.0.1:7000/page/$upcid/', 'type': 'api'}, 'Sim': {'url': 'http://127.0.0.1:7000/sim/', 'type': 'api'}, 'Google': {'url': 'http://www.google.com', 'type': 'service'}}
    for item in SSM_APP_CONFIG.cache.items:
        if item not in [FUNC_NAME, 'DEFAULT']:
            url = SSM_APP_CONFIG.get_param(item)["url"]
            print(item + ":" + url)
            for key in API_CONFIG:
                current = API_CONFIG[key]
                new_url = current["url"]
                if "service://" + item in new_url:
                    API_CONFIG[key]["url"] = new_url.replace("service://" + item, url)
    print(str(API_CONFIG))


print('The settings file has been loaded.')
