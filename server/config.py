# -*- coding: utf-8 -*-
"""
    Class to define the type of environment configutation
    * class      Config, DevelopmentConfig, TestingConfig, ProductionConfig
    * requires   python 3.+, PyQt5
    * version    1.0.0
    * package    icity_api
    * subpackage icity_api
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
"""
class Config:

    SECRET_KEY = None
    # SERVER_NAME = '127.0.0.1'
    # SERVER_PORT = 5736
    DB_SERVER = '191.241.192.43'
    DATABASE_DRIVER = 'postgresql'
    DEBUG = False
    TESTING = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SERVER_NAME = '127.0.0.1'
    DATABASE_DRIVER = 'sqlite'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SERVER_NAME = '127.0.0.1'
    DB_SERVER = '127.0.0.1'
    DATABASE_DRIVER = 'sqlite'


class ProductionConfig(Config):
    DEBUG = False

config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
