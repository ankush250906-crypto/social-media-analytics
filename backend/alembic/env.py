import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- FORCE ALEMBIC TO USE RENDER'S DATABASE_URL ---
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
# --------------------------------------------------

# Add your model's MetaData object here for 'autogenerate' support
from app.database import Base
from app.models import User, Post, CampaignMetric  # Ensure all models are imported
target_metadata = Base.metadata
