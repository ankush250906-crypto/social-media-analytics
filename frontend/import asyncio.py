import asyncio
import json
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.services.dataset_ingestion import DataRepository
from app.ai_engines.sentiment_engine import process_sentiment_trends

app = FastAPI(title="Social Media Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection Manager for WebSockets
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/analytics")
async def websocket_analytics_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        data_repo = DataRepository()
        df = data_repo.get_data()
        
        # Stream live analytics pulses every 3 seconds
        idx = 0
        while True:
            await asyncio.sleep(3)
            # Slice sample batch to simulate streaming data stream
            sample_batch = df.iloc[idx : idx + 5]
            idx = (idx + 5) % len(df)
            
            payload = {
                "event": "live_feed_update",
                "batch_size": len(sample_batch),
                "latest_posts": sample_batch[["post_id", "content", "sentiment_label", "likes_count"]].to_dict(orient="records"),
                "sentiment_summary": process_sentiment_trends(sample_batch)["sentiment_breakdown"]
            }
            await websocket.send_json(payload)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)