# config.py
"""
Application configuration using Pydantic BaseSettings.
Loads environment variables from a .env file.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
      Attributes
        database_url(str): takes the sqlite url
          eg: "sqlite:///./addresses.db"
    """
    database_url: str
    class Config:
        """
        Pydantic configuration for the Settings model.
        env_file (str): Path to the .env file to load environment variables.
            Example: ".env"
        """
        env_file = ".env"

# Singleton settings object to be imported anywhere
settings = Settings()