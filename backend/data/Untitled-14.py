# backend/test_production_health.py
import sys
import httpx

# Update with your live Render backend URL
PROD_API_URL = "https://social-analytics-api.onrender.com"

def run_production_health_check():
    print(f"🔍 Starting End-to-End Health Check for: {PROD_API_URL}\n")
    
    with httpx.Client(base_url=PROD_API_URL, timeout=10.0) as client:
        # 1. API Health Check Endpoint
        try:
            r = client.get("/health")
            assert r.status_code == 200
            print("✅ [1/4] FastAPI Server Health Endpoint: ONLINE")
        except Exception as e:
            print(f"❌ [1/4] FastAPI Health Endpoint Failed: {e}")
            sys.exit(1)

        # 2. Database & Auth Flow (Get JWT Token)
        try:
            auth_payload = {"username": "admin", "password": "analytics123"}
            r = client.post("/api/v1/auth/login", data=auth_payload)
            assert r.status_code == 200
            token = r.json().get("access_token")
            assert token is not None
            print("✅ [2/4] Auth & Database (PostgreSQL): AUTHENTICATED")
        except Exception as e:
            print(f"❌ [2/4] Database Authentication Failed: {e}")
            sys.exit(1)

        headers = {"Authorization": f"Bearer {token}"}

        # 3. Redis Caching & Sentiment Analytics Endpoint
        try:
            r = client.get("/api/v1/analytics/sentiment-summary", headers=headers)
            assert r.status_code == 200
            print("✅ [3/4] Redis Caching & Analytics Endpoint: FUNCTIONAL")
        except Exception as e:
            print(f"❌ [3/4] Redis Caching Failed: {e}")
            sys.exit(1)

        # 4. Async Task Trigger (Celery Worker Queue)
        try:
            r = client.post("/api/v1/reports/trigger-pdf", headers=headers)
            assert r.status_code in [200, 202]
            print("✅ [4/4] Celery Background Worker Queue: DISPATCHED")
        except Exception as e:
            print(f"❌ [4/4] Celery Task Trigger Failed: {e}")
            sys.exit(1)

    print("\n🎉 ALL PRODUCTION HEALTH CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_production_health_check()