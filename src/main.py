from src.database import SessionLocal
from src.models import Campaign, Post
from src.tasks import publish_post_task
from src.ai import AIEngine
import time

def main():
    db = SessionLocal()
    ai = AIEngine() # <--- Instantiate the Brain

    # --- Step 1: Input ---
    print("\n💡 New Campaign Idea: 'PromoBot Launch'")
    raw_draft = """
    I built a tool called PromoBot. 
    It uses Python, Redis, and Celery to automate social media posts.
    I learned a lot about the Strategy Pattern and Docker.
    It's open source and I want people to try it.
    """

    # --- Step 2: The AI Processing ---
    print("🧠 calling Gemini to generate Dev.to version...")
    
    # This is the magic moment - AI writes the code for us
    devto_content = ai.rewrite(raw_draft, platform="devto")
    
    print("\n✨ AI Generated Content Preview:")
    print("-" * 40)
    print(devto_content[:200] + "...") # Print first 200 chars
    print("-" * 40)

    # --- Step 3: Persistence ---
    campaign = Campaign(title="PromoBot Launch", original_markdown=raw_draft)
    db.add(campaign)
    db.commit()

    post = Post(
        campaign_id=campaign.id,
        platform="devto",
        final_content=devto_content, # <--- Saving the AI version!
        status="queued"
    )
    db.add(post)
    db.commit()
    
    # --- Step 4: Dispatch ---
    print(f"🚀 Dispatching AI-written post #{post.id} to Celery...")
    task = publish_post_task.delay(post.id)
    print(f"✅ Task Sent! ID: {task.id}")
    
    db.close()

if __name__ == "__main__":
    main()