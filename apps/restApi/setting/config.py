import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '20210418_UnripeData')
    TOKEN = ''
    HOST = '0.0.0.0'
    PORT = '80'
    DEBUG = False
    DUPLICATE_LOGIN = False

    MARIA_USER = ""
    MARIA_PWD = ""
    MARIA_HOST = ""
    MARIA_PORT = 3306
    MARIA_DB = ""

    REDIS_PWD = ""
    REDIS_HOST = ""
    REDIS_PORT = 9001


class DevConfig(Config):
    MARIA_HOST = ""
    MARIA_PORT = 10001

    REDIS_HOST = ""

    PORT = '5000'
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TEST = True


config_by_name = {
    'dev': DevConfig,
    'test': TestConfig,
    'publish': Config
}

config = config_by_name[os.getenv('FLASK_ENV') or 'dev']()
