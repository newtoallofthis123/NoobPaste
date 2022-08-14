import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '4357093cd57da6dad99b7314'
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "n_db")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    MAIL_SERVER =  'smtp.gmail.com'
    MAIL_PORT =  465
    MAIL_USE_TLS =  False
    MAIL_USE_SSL = True
    MAIL_USERNAME =  os.environ.get("mail_username")
    MAIL_PASSWORD =  os.environ.get("mail_password")


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ("postgresql://wziphjmqomxtog:7dd18881b7d26c0cb3b05f5dd6cb6b6103b012890c516e3e0a804d499619f000@ec2-34-193-44-192.compute-1.amazonaws.com:5432/d7d1q7g1f4sb96")


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True