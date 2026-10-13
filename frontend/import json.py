import json
import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

class CacheService:
    def __init__(self):
        try:
            self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
        except Exception as e:
            print(f"[Cache Warning]: Redis connection failed. {e}")
            self.client = None

    def get(self, key: str):
        if not self.client:
            return None
        data = self.client.get(key)
        return json.loads(data) if data else None

    def set(self, key: str, value: dict, ttl_seconds: int = 300):
        if self.client:
            self.client.setex(key, ttl_seconds, json.dumps(value))