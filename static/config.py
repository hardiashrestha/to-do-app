import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('ece038022f1f0188a9666e99962745a0') or 'your-default-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db'