"""Configuration management for the API wrapper."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    PORT = int(os.getenv("PORT", "8000"))
    HOST = os.getenv("HOST", "0.0.0.0")
    DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "claude")


config = Config()
