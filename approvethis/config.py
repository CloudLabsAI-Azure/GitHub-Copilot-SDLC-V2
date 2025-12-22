"""Application configuration."""
import os
from pathlib import Path

basedir = Path(__file__).parent.absolute()


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GITHUB_PROVIDER = os.environ.get('GITHUB_PROVIDER', 'mock')
    
    # Azure Function configuration
    AZURE_FUNCTION_URL = os.environ.get('AZURE_FUNCTION_URL')
    AZURE_FUNCTION_KEY_SECRET = os.environ.get('AZURE_FUNCTION_KEY_SECRET')
    
    @staticmethod
    def init_app(app):
        """Initialize application."""
        pass


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "approvethis.db"}'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "approvethis.db"}'
    
    @classmethod
    def init_app(cls, app):
        """Initialize production app."""
        Config.init_app(app)
        
        # Log to stderr in production
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
