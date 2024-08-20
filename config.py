import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    # Add other configurations here.

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Add other production configuration settings here.

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    # Add other development configuration settings here.

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    # Add other testing configuration settings here.