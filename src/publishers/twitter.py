from src.publishers.base import BasePublisher
from playwright.sync_api import sync_playwright
from src.config import logger, Config
import time

class TwitterPublisher(BasePublisher):
    def publish(self, content: dict) -> str:
        # --- SAFETY CHECK ---
        if len(content["body"]) > 280:
            logger.error(f"❌ Tweet too long ({len(content['body'])} chars). Skipping to avoid ban.")
            return None

        state_path = Config.TWITTER_STATE_PATH
        
        with sync_playwright() as p:
            logger.info("🐦 Launching X (Twitter)...")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state=state_path)
            page = context.new_page()

            page.goto("https://x.com/home")
            time.sleep(5) # Let feed load

            # Keyboard shortcut 'n' opens new tweet modal
            logger.info("⌨️ Pressing 'n' to tweet...")
            page.keyboard.press("n")
            time.sleep(2)

            # Type content
            logger.info("✍️ Typing tweet...")
            page.keyboard.insert_text(content["body"])
            
            # Click Post
            logger.info("👆 Clicking Post...")
            # X changes button text often ("Post", "Tweet", "Reply")
            post_btn = page.locator("button[data-testid='tweetButton']").first
            
            if post_btn.is_visible():
                post_btn.click()
                logger.info("✅ Tweet sent!")
                time.sleep(3)
                return "https://x.com/home" 
            else:
                logger.error("❌ Tweet button not found!")
                return None