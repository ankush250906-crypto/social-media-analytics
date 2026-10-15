# backend/alembic/env.py (around line 30-45)
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config

# --- ENSURE THIS IS PRESENT ---
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
# ------------------------------