# src/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database import Base

class Campaign(Base):
    """The Master Idea."""
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    original_markdown = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Post(Base):
    """The Platform Adaptation."""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    
    platform = Column(String) # 'devto', 'reddit'
    final_content = Column(Text) # The specific markdown for this platform
    status = Column(String, default="draft") # draft, published
    
    published_url = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())