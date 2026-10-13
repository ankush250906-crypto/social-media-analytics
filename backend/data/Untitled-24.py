# backend/app/main.py (addition)
from app.api import auth, analytics, reports, campaigns, websockets

app.include_router(websockets.router)