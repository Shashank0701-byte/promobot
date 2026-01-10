# src/main.py
from src.database import SessionLocal
from src.models import Campaign, Post
from src.tasks import publish_post_task
import time

def main():
    db = SessionLocal()

    print("📝 Creating Campaign in DB...")
    # 1. Create the Master Idea
    campaign = Campaign(
        title="Celery Test Campaign",
        original_markdown="# Async is cool\n\nThis runs in the background."
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    # 2. Create the Platform Adaptation
    post = Post(
        campaign_id=campaign.id,
        platform="devto",
        final_content="# Hello from Celery!\n\nI was processed by a worker.",
        status="queued"
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    
    print(f"💾 Saved Post #{post.id} to DB (Status: {post.status})")

    # 3. Dispatch the Task!
    print("🚀 Dispatching to Celery Worker...")
    task = publish_post_task.delay(post.id)
    
    print(f"✅ Task Sent! ID: {task.id}")
    print("Check your terminal logs to see the worker pick it up.")
    
    db.close()

if __name__ == "__main__":
    main()