from playwright.sync_api import sync_playwright
import os
import sys

# Ensure secrets directory exists
os.makedirs("secrets", exist_ok=True)

def capture_login(platform_name, url):
    filename = f"secrets/{platform_name}_state.json"
    
    with sync_playwright() as p:
        # Launch with Stealth Arguments to fool bot detection
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"] # <--- Vital for X/Twitter
        )
        
        # Use a real User Agent so we don't look like a script
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Extra Stealth: Hide the 'navigator.webdriver' property
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print(f"\n🤖 Opening {platform_name} ({url})...")
        print("👉 PLEASE LOG IN MANUALLY NOW.")
        print("   (You have 5 minutes. Close the browser window when you are done!)")
        
        page.goto(url)

        try:
            # Wait for you to close the browser manually
            page.wait_for_event("close", timeout=300000) 
            
            # Save the state
            context.storage_state(path=filename)
            print(f"✅ Success! Session saved to {filename}")
            
        except Exception as e:
            print(f"❌ Timed out or failed: {e}")
            try:
                context.storage_state(path=filename)
                print(f"⚠️ Attempted emergency save to {filename}")
            except:
                pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m tools.auth_universal [name] [url]")
    else:
        capture_login(sys.argv[1], sys.argv[2])