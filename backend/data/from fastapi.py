from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Active"
    assert "dataset_records" in data

def test_sentiment_endpoint():
    response = client.get("/api/v1/analytics/sentiment")
    assert response.status_code == 200
    data = response.json()
    assert "timeline" in data
    assert "sentiment_breakdown" in data

def test_demographics_endpoint():
    response = client.get("/api/v1/analytics/demographics")
    assert response.status_code == 200
    data = response.json()
    assert "geographic_distribution" in data

def test_trends_endpoint():
    response = client.get("/api/v1/analytics/trends")
    assert response.status_code == 200
    data = response.json()
    assert "trending_hashtags" in data

def test_network_endpoint():
    response = client.get("/api/v1/analytics/network")
    assert response.status_code == 200
    data = response.json()
    assert "graph_stats" in data
    assert "top_kols" in data