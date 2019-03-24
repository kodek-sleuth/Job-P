import os
class Config():
    SECRET_KEY='its nolonger a secret'
    SQLALCHEMY_TRACK_MODIFICATIONS=False 

class DevelopmentConfig(Config):
    DEBUG=True
    DEVELOPMENT=True
    SECRET_KEY='its nolonger a secret'
    SQLALCHEMY_DATABASE_URI='postgresql://business:businessonly@localhost:5432/portal'
    
class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG=True
    TESTING=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    USER_SECRET_KEY='i wont tell if you dont'
    ADMIN_SECRET_KEY='secret'
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:believe@localhost:5432/fortestsonly'


class ProductionConfig(Config):
    DEBUG=False
    TESTING=False
    SECRET_KEY='its nolonger a secret'
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS=False 

app_config={
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}