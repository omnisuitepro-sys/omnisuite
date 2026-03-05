import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, Text, Float,
    Enum, ForeignKey, Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -------------------------------------------------------------
# 1. DATABASE SELECTION
# -------------------------------------------------------------
# SQLite for local development - easiest setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "omni_core.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# For future VPS/PostgreSQL:
# DATABASE_URL = "postgresql+psycopg2://username:password@localhost/omnirecall"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
from backend.core.db_base import Base

# -------------------------------------------------------------
# 2. TABLE: Licenses
# -------------------------------------------------------------
class License(Base):
    __tablename__ = "licenses"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    tier = Column(String, default="Free")
    expiry = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

# -------------------------------------------------------------
# 3. TABLE: Pending Trades
# -------------------------------------------------------------
class PendingTrade(Base):
    __tablename__ = "pending_trades"
    id = Column(Integer, primary_key=True, index=True)
    trade_id = Column(String, unique=True, index=True)
    symbol = Column(String)
    side = Column(String)
    reason = Column(Text)
    status = Column(String, default="pending_approval")
    created_at = Column(DateTime, default=datetime.utcnow)

# -------------------------------------------------------------
# 4. TABLE: System Logs
# -------------------------------------------------------------
class SystemLog(Base):
    __tablename__ = "system_logs"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String, default="core")

# -------------------------------------------------------------
# 5. INITIALIZATION METHOD
# -------------------------------------------------------------
def init_database():
    print("🧩  Initializing Omni Core database...")
    Base.metadata.create_all(bind=engine)
    print(f"✅  Database ready: {DB_PATH}")

if __name__ == "__main__":
    init_database()

from sqlalchemy import create_engine
from backend.finance.models import Base

engine = create_engine(
    "sqlite:///C:/OmniSuite/backend/omni_core.db", echo=True, future=True
)

Base.metadata.create_all(bind=engine)
print("✅  Database ready:", os.path.abspath("backend/omni_core.db"))