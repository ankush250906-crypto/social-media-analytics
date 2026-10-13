import pandas as pd

def process_sentiment_trends(df: pd.DataFrame):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    timeline = df.set_index('timestamp').resample('D').agg({
        'sentiment_score': 'mean',
        'toxicity_score': 'mean',
        'likes_count': 'sum',
        'post_id': 'count'
    }).reset_index()
    
    timeline['timestamp'] = timeline['timestamp'].dt.strftime('%Y-%m-%d')
    timeline = timeline.rename(columns={'post_id': 'volume'}).fillna(0)
    
    return {
        "timeline": timeline.to_dict(orient='records'),
        "emotions": df['emotion_type'].value_counts().to_dict(),
        "sentiment_breakdown": df['sentiment_label'].value_counts().to_dict()
    }   