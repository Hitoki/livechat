import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'livechat.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'pofk84z0bl9g14k0f'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql:///livechat"
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    # SQLALCHEMY_DATABASE_URI = "postgresql:///livechat"
    DEBUG = True
    TESTING = False
    GOOGLE_TRACK_ID = 'UA-75377135-1'
    LIVECHAT_LOGIN = 'vitaliy.romanuik@anvil8.com'
    LIVECHAT_API_KEY = '4655f8e27c49c371d585bc857ecf5ebc'
    TEST_L = 'andy@yomdel.com'
    TEST_K = '099b9ae6e46c6f74e964dd8dc1e067a3'