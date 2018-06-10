class Config():
    """
    Base Configuration
    """

    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/company_db'

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_ECHO = True
    DEBUG = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}