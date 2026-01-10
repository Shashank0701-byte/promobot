# src/main.py
from src.publishers.devto import DevtoPublisher

def main():
    # 1. Define the content (In Phase 2, this comes from the DB/Streamlit)
    post_data = {
        "title": "Automating My Life with Python (PromoBot Phase 1)",
        "body": """
        # Hello World!
        
        This post was created automatically by my custom tool, **PromoBot**.
        
        ## Architecture
        - **Language:** Python 3.11
        - **Pattern:** Strategy Pattern (Plugins)
        - **Target:** Dev.to API
        
        Stay tuned for Phase 2 where I add AI!
        """,
        "tags": ["python", "automation", "learning"]
    }

    # 2. Instantiate the publisher
    # In the future, we can loop through a list: [DevtoPublisher(), RedditPublisher()]
    publisher = DevtoPublisher()

    # 3. Execute
    url = publisher.publish(post_data)

    if url:
        print(f"\n✨ Success! View your draft here: {url}")
    else:
        print("\n💀 Mission Failed.")

if __name__ == "__main__":
    main()