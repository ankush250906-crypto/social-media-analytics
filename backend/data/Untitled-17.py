# backend/app/main.py (addition)
from app.api import auth, analytics, reports, campaigns

# Include routers
app.include_router(auth.router)
app.include_router(analytics.router)
app.include_router(reports.router)
app.include_router(campaigns.router)  # <-- Added here