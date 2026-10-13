# backend/app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class CampaignMetric(Base):
    __tablename__ = "campaign_metrics"

    id = Column(Integer, primary_key=True, index=True)
    campaign_name = Column(String, index=True, nullable=False)
    platform = Column(String, nullable=False)  # e.g., Twitter, LinkedIn, Instagram
    engagement_rate = Column(Float, default=0.0)
    sentiment_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())