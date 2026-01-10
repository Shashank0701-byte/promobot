import requests
import json
from src.config import Config, logger

class AIEngine:
    """
    The Intelligence Layer.
    Uses Google Gemini 2.5 Flash via raw REST API to rewrite content.
    """
    
    # We use the 'flash' model because it's fast and cheap for text rewriting
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    def rewrite(self, draft: str, platform: str) -> str:
        """
        Rewrites a master draft for a specific platform.
        """
        logger.info(f"🧠 Asking Gemini to rewrite draft for {platform}...")

        # 1. Construct the Prompt (The "System Design" of AI)
        prompt = self._build_prompt(draft, platform)

        # 2. Build Payload
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        # 3. Fire Request
        try:
            url = f"{self.BASE_URL}?key={Config.GEMINI_API_KEY}"
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            # 4. Parse Response (Safely)
            data = response.json()
            generated_text = data['candidates'][0]['content']['parts'][0]['text']
            
            return generated_text.strip()

        except Exception as e:
            logger.error(f"❌ AI Brain Freeze: {e}")
            # Fallback: If AI fails, just return the original draft so we don't crash
            return draft

    def _build_prompt(self, draft: str, platform: str) -> str:
        """
        Factory method to generate specific prompts per platform.
        """
        if platform == "devto":
            return (
                f"You are a technical editor. Rewrite the following text as a high-quality "
                f"Dev.to article. Use Markdown. Add a catchy title at the top with '# '. "
                f"Keep it technical.\n\n"
                f"ORIGINAL TEXT:\n{draft}"
            )
        elif platform == "reddit":
            return (
                f"You are a Redditor. Rewrite this text to be casual and humble. "
                f"Use 'I' statements. Keep it under 200 words. "
                f"CRITICAL RULE: DO NOT INCLUDE ANY URLS, LINKS, OR HTTP ADDRESSES. "
                f"Plain text only. Do not mention 'Link in comments'.\n\n"
                f"ORIGINAL TEXT:\n{draft}"
            )
        elif platform == "linkedin":
             return (
                f"Rewrite this for LinkedIn. Professional but engaging tone. "
                f"Focus on the 'achievement' and 'engineering challenges'. "
                f"Use bullet points and appropriate hashtags.\n\n"
                f"ORIGINAL TEXT:\n{draft}"
            )
        else:
            return f"Rewrite this text:\n{draft}"