from src.database import SessionLocal
from src.models import Campaign, Post
from src.tasks import publish_post_task
from src.ai import AIEngine
from src.publishers.reddit import RedditPublisher
import time

def main():
    db = SessionLocal()
    ai = AIEngine()

    # --- Step 1: Input (The Master Idea) ---
    print("\n💡 New Campaign Idea: 'PromoBot Phase 2'")
    raw_draft = """
    I just updated PromoBot to support Reddit! 
    It now uses Playwright to automate the browser because Reddit's API is strict.
    I'm using the Factory Pattern to switch between Dev.to (API) and Reddit (Browser).
    The architecture is Python + Redis + Celery + Docker.
    It's honestly pretty cool watching the ghost browser type for me.
    """

    # ==========================================
    # 🟢 PLATFORM 1: DEV.TO (Background API)
    # ==========================================
    print("\n[1/2] 🧠 Generating Dev.to article via Gemini...")
    devto_content = ai.rewrite(raw_draft, platform="devto")
    
    # Save to DB
    campaign = Campaign(title="PromoBot Phase 2", original_markdown=raw_draft)
    db.add(campaign)
    db.commit()

    post_devto = Post(
        campaign_id=campaign.id,
        platform="devto",
        final_content=devto_content,
        status="queued"
    )
    db.add(post_devto)
    db.commit()
    
    # Dispatch to Celery
    print(f"🚀 Dispatching Dev.to Post #{post_devto.id} to Celery Worker...")
    publish_post_task.delay(post_devto.id)


    # ==========================================
    # 🟠 PLATFORM 2: REDDIT (Foreground Browser)
    # ==========================================
    print("\n[2/2] 🧠 Generating Reddit post via Gemini...")
    reddit_content = ai.rewrite(raw_draft, platform="reddit")
    
    # Save to DB
    post_reddit = Post(
        campaign_id=campaign.id,
        platform="reddit",
        target_audience="u_Particular-Run1230", # Posting to your profile first!
        final_content=reddit_content,
        status="processing"
    )
    db.add(post_reddit)
    db.commit()

    print("\n👀 Get ready! Launching Browser in 3 seconds to post to Reddit...")
    print("   (Don't touch the mouse/keyboard while it runs!)")
    time.sleep(3)

    try:
        # We run this DIRECTLY (not Celery) so you can watch it happen
        publisher = RedditPublisher()
        
        # Construct the payload
        reddit_payload = {
            "title": "I built a bot to post this automatically (PromoBot Update)",
            "body": reddit_content,
            "subreddit": "u_Particular-Run1230" 
        }
        
        url = publisher.publish(reddit_payload)
        
        if url:
            print(f"🎉 SUCCESS! Posted to Reddit: {url}")
            post_reddit.status = "published"
            post_reddit.published_url = url
        else:
            print("❌ Failed to post to Reddit.")
            post_reddit.status = "failed"
            
    except Exception as e:
        print(f"💥 CRITICAL ERROR: {e}")
        post_reddit.status = "error"
    
    db.commit()
    db.close()

if __name__ == "__main__":
    main()