# src/publishers/devto.py
import requests
from src.config import Config, logger
from src.publishers.base import BasePublisher
from typing import Dict, Any

class DevtoPublisher(BasePublisher):
    """
    Handles publishing to Dev.to API.
    Docs: https://developers.forem.com/api/v1#tag/articles/operation/createArticle
    """
    
    BASE_URL = "https://dev.to/api/articles"

    def publish(self, content: Dict[str, Any]) -> str:
        headers = {
            "Content-Type": "application/json",
            "api-key": Config.DEVTO_API_KEY
        }
        
        # Map our generic content dict to Dev.to's specific payload structure
        payload = {
            "article": {
                "title": content.get("title"),
                "body_markdown": content.get("body"),
                "published": False,  # Always draft first for safety
                "tags": content.get("tags", []),
                "series": "PromoBot Automation"
            }
        }

        try:
            logger.info(f"🚀 Attempting to publish to Dev.to: {content.get('title')}")
            response = requests.post(self.BASE_URL, json=payload, headers=headers)
            response.raise_for_status() # Raises HTTPError for bad responses (4xx, 5xx)
            
            data = response.json()
            url = data.get("url")
            logger.info(f"✅ Successfully created draft: {url}")
            return url

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to publish to Dev.to: {e}")
            if hasattr(e, 'response') and e.response is not None:
                 logger.error(f"Server Response: {e.response.text}")
            return None