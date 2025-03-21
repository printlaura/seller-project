import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_fallback_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql+psycopg2://postgres:postgres@localhost/seller_project')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
