# Configuration for AI Worker
import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Configuration settings for the AI worker"""
    
    # Google Gemini API Configuration
    GEMINI_API_KEY: str = Field(..., description="Google Gemini API key")
    
    # RabbitMQ Configuration
    RABBITMQ_URL: str = Field(default="amqp://localhost:5672/", description="RabbitMQ connection URL")
    
    # Backend API Configuration
    BACKEND_URL: str = Field(default="http://localhost:8000", description="Backend API base URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()

