import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'livechat.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'pofk84z0bl9g14k0f'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    GOOGLE_TRACK_ID = 'UA-75377135-1'
    LIVECHAT_LOGIN = 'kidomakai@gmail.com'
    LIVECHAT_API_KEY = 'd68ed9aac8511fedb315199228bfb03c'