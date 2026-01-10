# src/tasks.py
from src.celery_app import app
from src.publishers.devto import DevtoPublisher
from src.database import SessionLocal
from src.models import Post
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@app.task(bind=True, max_retries=3)
def publish_post_task(self, post_id: int):
    """
    Background task to publish a specific post.
    """
    db = SessionLocal()
    try:
        # 1. Fetch the post from the DB
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            logger.error(f"Post {post_id} not found!")
            return "Failed: Post not found"

        logger.info(f"⚡ Processing Task: Publishing Post #{post.id} to {post.platform}")

        # 2. Select the right publisher
        # (Later we will use a Factory Pattern here)
        url = None
        if post.platform == "devto":
            publisher = DevtoPublisher()
            # Construct the payload expected by the publisher
            content = {
                "title": f"[{post.platform.upper()}] " + post.final_content[:30] + "...", # Simplified title logic
                "body": post.final_content,
                "tags": ["automation", "python"] # In real app, store tags in DB
            }
            url = publisher.publish(content)

        # 3. Update the DB with the result
        if url:
            post.status = "published"
            post.published_url = url
            post.updated_at = datetime.utcnow()
            db.commit()
            return f"Success: {url}"
        else:
            post.status = "failed"
            db.commit()
            # Retry if it failed (e.g., API timeout)
            raise self.retry(countdown=60)

    except Exception as e:
        logger.exception(f"Task Failed: {e}")
        post.status = "error"
        db.commit()
        raise e
    finally:
        db.close()