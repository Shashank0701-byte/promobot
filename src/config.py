import os
from dotenv import load_dotenv
import logging
from pathlib import Path

# 1. Define Root Path (Global)
ROOT_PATH = Path("D:/AutoPython/promobot") 

# 2. Load .env
load_dotenv(ROOT_PATH / ".env")

# 3. Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PromoBot")

class Config:
    """Central Configuration"""
    
    # --- FIX IS HERE: Add this line! ---
    PROMOBOT_HOME = ROOT_PATH 
    # -----------------------------------

    DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Pre-calculated paths for convenience
    REDDIT_STATE_PATH = ROOT_PATH / "secrets/reddit_state.json"
    TWITTER_STATE_PATH = ROOT_PATH / "secrets/twitter_state.json"
    PEERLIST_STATE_PATH = ROOT_PATH / "secrets/peerlist_state.json"

    @classmethod
    def validate(cls):
        if not cls.DEVTO_API_KEY:
            raise ValueError("❌ Missing DEVTO_API_KEY")
        if not cls.GEMINI_API_KEY:
            raise ValueError("❌ Missing GEMINI_API_KEY")

Config.validate()