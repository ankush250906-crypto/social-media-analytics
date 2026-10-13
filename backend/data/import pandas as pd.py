import pandas as pd
from app.ai_engines.sentiment_engine import process_sentiment_trends
from app.ai_engines.trend_engine import process_trending_topics

def test_sentiment_engine_logic():
    sample_df = pd.DataFrame([{
        "timestamp": "2026-01-01 10:00:00",
        "sentiment_score": 0.8,
        "toxicity_score": 0.0,
        "likes_count": 15,
        "post_id": 1,
        "emotion_type": "Joy",
        "sentiment_label": "Positive"
    }])
    
    result = process_sentiment_trends(sample_df)
    assert len(result["timeline"]) == 1
    assert result["sentiment_breakdown"]["Positive"] == 1

def test_trend_engine_logic():
    sample_df = pd.DataFrame([{
        "hashtags": "AI, Tech, Python",
        "topic_category": "Technology"
    }])
    
    result = process_trending_topics(sample_df)
    assert "AI" in result["trending_hashtags"]
    assert result["top_categories"]["Technology"] == 1