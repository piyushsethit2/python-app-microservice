"""
Configuration settings for the ML Microservice
"""
import os
from typing import Optional

class Config:
    """Configuration class for ML microservice"""
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5001))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Model settings
    HF_MODEL_NAME = os.getenv('HF_MODEL_NAME', 'distilbert-base-uncased')
    DEVICE = os.getenv('DEVICE', 'cpu')  # 'cpu' or 'cuda'
    
    # Request settings
    TIMEOUT = int(os.getenv('TIMEOUT', 30))
    MAX_LENGTH = int(os.getenv('MAX_LENGTH', 512))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_model_name(cls) -> str:
        """Get the model name with fallback"""
        return cls.HF_MODEL_NAME
    
    @classmethod
    def get_device(cls) -> str:
        """Get the device to use for inference"""
        return cls.DEVICE
    
    @classmethod
    def get_server_config(cls) -> dict:
        """Get server configuration"""
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'debug': cls.DEBUG
        } 