import os
from pathlib import Path

class Config:
    # Base configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    HOST = os.environ.get('GOLINKS_HOST', '0.0.0.0')
    PORT = int(os.environ.get('GOLINKS_PORT', 8080))
    
    # Application directory
    GOLINKS_DIR = os.path.join(str(Path.home()), '.golinks')
    
    # Database
    DB_NAME = 'golinks.db'
    DB_PATH = os.path.join(GOLINKS_DIR, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Logging
    LOG_FILE = os.path.join(GOLINKS_DIR, 'golinks.log')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @staticmethod
    def init_app(app):
        # Create golinks directory if it doesn't exist
        os.makedirs(Config.GOLINKS_DIR, exist_ok=True)
