from playwright.sync_api import sync_playwright
import time
import os

# Ensure secrets directory exists
os.makedirs("secrets", exist_ok=True)

def capture_login():
    with sync_playwright() as p:
        # headless=False means "Show me the browser UI"
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context()
        page = context.new_page()

        print("🤖 Opening Reddit... Please Log In manually in the browser window.")
        page.goto("https://www.reddit.com/login/")

        # Wait until we see the "Create Post" button or user avatar, 
        # indicating successful login.
        try:
            # Wait up to 300 seconds (5 mins) for you to handle 2FA/Captchas
            page.wait_for_url("https://www.reddit.com/", timeout=300000) 
            print("✅ Detected login! Saving cookies...")
            
            # Save the state (Cookies, LocalStorage)
            context.storage_state(path="secrets/reddit_state.json")
            print("💾 Session saved to secrets/reddit_state.json")
            
        except Exception as e:
            print(f"❌ Timed out or failed: {e}")
        
        browser.close()

if __name__ == "__main__":
    capture_login()