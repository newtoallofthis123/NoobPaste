import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '4372093cd57da6dad99b7314'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        "postgres://noobscience:hBHDIXxW6Xp4QxCe7G2Ltp4VdrLgkECS@dpg-ccjbafarrk09pi2kdvog-a.oregon-postgres.render.com/np_db"
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        "postgres://noobscience:hBHDIXxW6Xp4QxCe7G2Ltp4VdrLgkECS@dpg-ccjbafarrk09pi2kdvog-a.oregon-postgres.render.com/np_db"
    )

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True