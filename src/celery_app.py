# src/celery_app.py
from celery import Celery
import os

# Define the Redis URL (from docker-compose service name 'redis')
# If running locally (outside docker), use localhost. Inside docker, use 'redis'.
# We use a trick: os.getenv default allows it to work in both.
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "promobot",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.tasks"]  # We will create this file next
)

# Optional: Configure robust settings
app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

if __name__ == "__main__":
    app.start()