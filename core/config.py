import os

class Config:
    DEBUG = True
    SECRET_KEY = 'Girafa#2025!Flask'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/hortfruti'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}