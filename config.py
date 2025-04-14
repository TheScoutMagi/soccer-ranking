import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # Database configuration
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = quote_plus(os.environ.get('DB_PASSWORD', ''))  # URL encode the password
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'soccer_rankings')
    
    # Flag to switch between local and Cloud SQL
    USE_CLOUD_SQL = os.environ.get('USE_CLOUD_SQL', 'false').lower() == 'true'
    
    # Cloud SQL specific settings
    CLOUD_SQL_CONNECTION_NAME = os.environ.get('CLOUD_SQL_CONNECTION_NAME', '')
    
    @staticmethod
    def get_database_uri():
        if Config.USE_CLOUD_SQL:
            # When running on Cloud Run or App Engine
            if os.getenv('K_SERVICE') or os.getenv('GAE_ENV'):
                socket_path = '/cloudsql/{}'.format(Config.CLOUD_SQL_CONNECTION_NAME)
                return f'postgresql+psycopg2://{Config.DB_USER}:{Config.DB_PASSWORD}@/{Config.DB_NAME}?host={socket_path}'
            # When running locally with Cloud SQL Proxy
            else:
                return f'postgresql+psycopg2://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}'
        else:
            # Local PostgreSQL database
            return f'postgresql+psycopg2://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}' 