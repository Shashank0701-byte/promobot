from src.publishers.base import BasePublisher
from playwright.sync_api import sync_playwright
from src.config import logger, Config
import time

class PeerlistPublisher(BasePublisher):
    def publish(self, content: dict) -> str:
        state_path = Config.PEERLIST_STATE_PATH
        
        with sync_playwright() as p:
            logger.info("🟢 Launching Peerlist...")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state=state_path)
            page = context.new_page()

            page.goto("https://peerlist.io/scroll")
            time.sleep(5) # Give it time to load

            logger.info("✍️ Finding input box...")
            try:
                # STRATEGY 1: Look for the specific "Write Article" button
                write_btn = page.get_by_role("button", name="Write Article")
                
                # STRATEGY 2: Look for the placeholder text "Ask a question"
                ask_input = page.get_by_placeholder("Ask a question", exact=False)

                if write_btn.is_visible():
                    write_btn.click()
                elif ask_input.is_visible():
                    ask_input.click()
                else:
                    # Fallback: Click the generic container
                    page.locator("div[class*='create-post']").first.click()

                time.sleep(2)
                
                # Type the content
                page.keyboard.insert_text(content["body"])
                time.sleep(2)
                
                # Click Post (Looking for Green button or specific text)
                logger.info("👆 Clicking Post...")
                post_btn = page.locator("button.bg-green-500").or_(page.get_by_role("button", name="Post"))
                post_btn.first.click()
                
                logger.info("✅ Posted to Peerlist!")
                time.sleep(3)
                return "https://peerlist.io/scroll"

            except Exception as e:
                logger.error(f"❌ Failed Peerlist post: {e}")
                return None