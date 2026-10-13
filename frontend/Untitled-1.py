from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SocialPostModel(Base):
    __tablename__ = "social_posts"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String, unique=True, index=True)
    user_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    platform = Column(String, index=True)
    content = Column(String)
    sentiment_score = Column(Float)
    sentiment_label = Column(String)
    toxicity_score = Column(Float)
    emotion_type = Column(String)
    likes_count = Column(Integer, default=0)
    hashtags = Column(String, nullable=True)
    location = Column(String, nullable=True)