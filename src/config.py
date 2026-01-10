# src/config.py
import os
from dotenv import load_dotenv
import logging

# Load the .env file immediately
load_dotenv()

# Setup Logging (Print is for amateurs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PromoBot")

class Config:
    """Centralized configuration."""
    DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")

    @classmethod
    def validate(cls):
        """Ensure all required keys are present."""
        if not cls.DEVTO_API_KEY:
            logger.error("❌ Missing DEVTO_API_KEY in .env file")
            raise ValueError("Configuration Error: Missing API Keys")

# Run validation on import to fail fast
Config.validate()