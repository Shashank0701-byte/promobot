import requests
import json
import time
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

        # 1. Construct the Prompt
        prompt = self._build_prompt(draft, platform)

        # 2. Build Payload
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        # 3. Fire Request with RETRY LOGIC
        url = f"{self.BASE_URL}?key={Config.GEMINI_API_KEY}"
        
        for attempt in range(3):
            try:
                response = requests.post(url, json=payload)
                
                # Handle Rate Limiting (429)
                if response.status_code == 429:
                    wait_time = (attempt + 1) * 5
                    logger.warning(f"⚠️ Rate Limit Hit (429). Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                
                # 4. Parse Response
                data = response.json()
                generated_text = data['candidates'][0]['content']['parts'][0]['text']
                return generated_text.strip()

            except Exception as e:
                logger.error(f"❌ AI Attempt {attempt+1} failed: {e}")
                time.sleep(2)

        # Fallback if all attempts fail
        logger.error("💀 AI is dead. Using generic fallback.")
        return "Check out my new project! It's open source. #IndieHacker #Python"

    def _build_prompt(self, draft: str, platform: str) -> str:
        if platform == "devto":
            return (
                "You are a technical editor. Rewrite this as a Dev.to article (Markdown). "
                "Title starts with '# '. Technical and tutorial tone.\n\n"
                f"ORIGINAL:\n{draft[:2000]}"
            )
        elif platform == "reddit":
            return (
                "Rewrite this for Reddit (r/SideProject). Casual, humble, 'I' statements. "
                "Under 200 words. NO LINKS allowed in text.\n\n"
                f"ORIGINAL:\n{draft[:2000]}"
            )
        elif platform == "twitter":
            return (
                "Rewrite this as a Tweet. "
                "CRITICAL RULE: Total length MUST be under 200 characters. "
                "Do not use the full 280 limit. "
                "Use 2-3 hashtags. No links.\n\n"
                f"ORIGINAL:\n{draft[:2000]}"
            )
        elif platform == "peerlist":
            return (
                "Rewrite this for Peerlist.io. Tone: 'Maker/Indie Hacker'. "
                "Short paragraph format. NO LINKS.\n\n"
                f"ORIGINAL:\n{draft[:2000]}"
            )
        else:
            return f"Rewrite this text:\n{draft[:2000]}"