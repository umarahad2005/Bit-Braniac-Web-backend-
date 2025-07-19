"""
Configuration module for BitBraniac backend
Handles environment variables and application settings
"""

import os
from typing import Optional

class Config:
    """Application configuration class"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'bitbraniac-secret-key-2024')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Google API settings
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Gemini model settings
    MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-2.0-flash')
    MODEL_TEMPERATURE = float(os.getenv('MODEL_TEMPERATURE', '0.8'))
    MAX_OUTPUT_TOKENS = int(os.getenv('MAX_OUTPUT_TOKENS', '8192'))
    
    # Memory settings
    CONVERSATION_WINDOW_SIZE = int(os.getenv('CONVERSATION_WINDOW_SIZE', '10'))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate required configuration
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not cls.GOOGLE_API_KEY:
            print("Warning: GOOGLE_API_KEY not set. Using default key for demo.")
            return False
        return True
    
    @classmethod
    def get_google_api_key(cls) -> str:
        """
        Get Google API key with fallback
        
        Returns:
            Google API key
        """
        return cls.GOOGLE_API_KEY or "AIzaSyD1q-8NDNoiHSzJO8JvdYmWUBgUVv4n9Vs"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: Optional[str] = None) -> Config:
    """
    Get configuration based on environment
    
    Args:
        config_name: Configuration name (development, production)
        
    Returns:
        Configuration class
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    return config_map.get(config_name, DevelopmentConfig)

