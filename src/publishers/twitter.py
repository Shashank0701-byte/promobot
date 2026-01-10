from src.publishers.base import BasePublisher
from playwright.sync_api import sync_playwright
from src.config import logger, Config
import time

class TwitterPublisher(BasePublisher):
    def publish(self, content: dict) -> str:
        state_path = Config.PROMOBOT_HOME / "secrets/twitter_state.json"
        
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
            # We look for the blue button in the dialog
            post_btn = page.locator("button[data-testid='tweetButton']").first
            
            if post_btn.is_visible():
                post_btn.click()
                logger.info("✅ Tweet sent!")
                time.sleep(3)
                return "https://x.com/home" # Can't easily get exact link without complex scraping
            else:
                logger.error("❌ Tweet button not found!")
                return None