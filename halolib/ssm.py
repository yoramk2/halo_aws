from __future__ import print_function

import configparser
import datetime
import json
import logging
import os
import time

import boto3
from botocore.exceptions import ClientError

from .const import settingsx
from .exceptions import HaloError, CacheKeyError, CacheExpireError
from .logs import log_json

# from django.conf import settings
settings = settingsx()

current_milli_time = lambda: int(round(time.time() * 1000))

logger = logging.getLogger(__name__)

# Initialize boto3 client at global scope for connection reuse
client = boto3.client('ssm', region_name=settings.AWS_REGION)
env = os.environ['HALO_STAGE']
app_config_path = os.environ['HALO_CONFIG_PATH']
app_name = os.environ['HALO_APP_NAME']
full_config_path = '/' + app_name + '/' + env + '/' + app_config_path
short_config_path = '/' + app_name + '/' + env


class Cache(object):
    expiration = 0
    items = None


DEFAULT_EXPIRY = 3 * 60 * 1000;  # default expiry is 3 mins


def load_cache(config, expiryMs=DEFAULT_EXPIRY):
    if config is None:
        raise HaloError('you need to provide a non-empty config')

    if (expiryMs <= 0):
        raise HaloError('you need to specify an expiry (ms) greater than 0, or leave it undefined')

    # the below uses the captured closure to return an object with a gettable
    # property per config key that on invoke:
    #  * fetch the config values and cache them the first time
    #  * thereafter, use cached values until they expire
    #  * otherwise, try fetching from SSM parameter store again and cache them

    now = datetime.datetime.now()
    cache = Cache()
    cache.expiration = current_milli_time() + expiryMs
    cache.items = config

    logger.debug('refreshed cache')
    return cache


class MyConfig:
    def __init__(self, cache, path):
        """
        Construct new MyApp with configuration
        :param config: application configuration
        """
        self.cache = cache
        self.path = path

    def get_param(self, key):
        now = current_milli_time()
        if now <= self.cache.expiration:
            if key in self.cache.items:
                return self.cache.items[key]
            else:
                raise CacheKeyError("no key in cache:" + key)
        else:
            self.cache = get_cache(self.path)
            if key in self.cache.items:
                return self.cache.items[key]
        raise CacheExpireError("cache expired")


def load_config(ssm_parameter_path):
    """
    Load configparser from config stored in SSM Parameter Store
    :param ssm_parameter_path: Path to app config in SSM Parameter Store
    :return: ConfigParser holding loaded config
    """
    configuration = configparser.ConfigParser()
    try:
        # Get all parameters for this app
        param_details = client.get_parameters_by_path(
            Path=ssm_parameter_path,
            Recursive=False,
            WithDecryption=True
        )

        # Loop through the returned parameters and populate the ConfigParser
        if 'Parameters' in param_details and len(param_details.get('Parameters')) > 0:
            for param in param_details.get('Parameters'):
                param_path_array = param.get('Name').split("/")
                section_position = len(param_path_array) - 1
                section_name = param_path_array[section_position]
                config_values = json.loads(param.get('Value'))
                config_dict = {section_name: config_values}
                logger.debug("Found configuration: " + str(config_dict))
                configuration.read_dict(config_dict)

    except ClientError as e:
        logger.error("Encountered an error loading config from SSM.",
                     extra=log_json(req_context={}, params={"path": ssm_parameter_path}, err=e))
    finally:
        return configuration


def get_cache(path):
    config = load_config(path)
    cache = load_cache(config)
    return cache

def get_config():
    # Initialize app if it doesn't yet exist
    logger.debug("Loading config and creating new MyConfig...")
    cache = get_cache(full_config_path)
    myconfig = MyConfig(cache, full_config_path)
    logger.debug("MyConfig is " + str(cache.items._sections))
    return myconfig

def get_app_config():
    # Initialize app if it doesn't yet exist
    logger.debug("Loading app config and creating new AppConfig...")
    cache = get_cache(short_config_path)
    appconfig = MyConfig(cache, short_config_path)
    logger.debug("AppConfig is " + str(cache.items._sections))
    return appconfig
