from src.publishers.base import BasePublisher
from playwright.sync_api import sync_playwright
from src.config import logger, Config
import time

class PeerlistPublisher(BasePublisher):
    def publish(self, content: dict) -> str:
        state_path = Config.PROMOBOT_HOME / "secrets/peerlist_state.json"
        
        with sync_playwright() as p:
            logger.info("🟢 Launching Peerlist...")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state=state_path)
            page = context.new_page()

            # Go to the scroll (feed)
            page.goto("https://peerlist.io/scroll")
            time.sleep(4)

            # Click "What are you working on?" input
            logger.info("✍️ Finding input box...")
            # Peerlist usually has a placeholder div or textarea
            try:
                page.get_by_placeholder("What are you working on?").click()
                time.sleep(1)
                page.keyboard.insert_text(content["body"])
                time.sleep(2)
                
                # Click Post
                logger.info("👆 Clicking Post...")
                page.get_by_role("button", name="Post").click()
                
                logger.info("✅ Posted to Peerlist!")
                time.sleep(3)
                return "https://peerlist.io/scroll"
            except Exception as e:
                logger.error(f"❌ Failed Peerlist post: {e}")
                return None