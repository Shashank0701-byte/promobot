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
        if platform == "devto":
            return (
                "You are a technical editor. Rewrite this as a Dev.to article (Markdown). "
                "Title starts with '# '. Technical and tutorial tone.\n\n"
                f"ORIGINAL:\n{draft}"
            )
        elif platform == "reddit":
            return (
                "Rewrite this for Reddit (r/SideProject). Casual, humble, 'I' statements. "
                "Under 200 words. NO LINKS allowed in text.\n\n"
                f"ORIGINAL:\n{draft}"
            )
        elif platform == "twitter":
            return (
                "Rewrite this as a viral Tweet. Short, punchy, under 280 characters. "
                "Use 2-3 relevant hashtags. Emojis allowed. NO LINKS (I will add it later).\n\n"
                f"ORIGINAL:\n{draft}"
            )
        elif platform == "peerlist":
            return (
                "Rewrite this for Peerlist.io. Tone: 'Maker/Indie Hacker'. "
                "Professional but enthusiastic. Focus on 'shipping' and 'building'. "
                "Short paragraph format. NO LINKS.\n\n"
                f"ORIGINAL:\n{draft}"
            )
        else:
            return f"Rewrite this text:\n{draft}"