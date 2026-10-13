from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.dataset_ingestion import DataRepository
from app.ai_engines.sentiment_engine import process_sentiment_trends
from app.ai_engines.demographic_engine import process_demographic_insights
from app.ai_engines.trend_engine import process_trending_topics
from app.ai_engines.network_engine import build_network_graph

app = FastAPI(title="Social Media Analytics Framework", version="1.0.0")

# Enable CORS for Next.js/React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = DataRepository()

@app.get("/")
def root():
    return {"status": "Active", "dataset_records": len(repo.get_data())}

@app.get("/api/v1/analytics/sentiment")
def get_sentiment_analytics():
    df = repo.get_data()
    return process_sentiment_trends(df)

@app.get("/api/v1/analytics/demographics")
def get_demographics():
    df = repo.get_data()
    return process_demographic_insights(df)

@app.get("/api/v1/analytics/trends")
def get_trends():
    df = repo.get_data()
    return process_trending_topics(df)

@app.get("/api/v1/analytics/network")
def get_network_topology():
    df = repo.get_data()
    return build_network_graph(df)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)