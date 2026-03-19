import os
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, func
from sqlalchemy.orm import relationship, declarative_base
from backend.db_session import engine

# ---------- Base Class ----------
Base = declarative_base()

# ---------- Example Tables ----------
class License(Base):
    __tablename__ = "licenses"

    id = Column(Integer, primary_key=True, index=True)
    license_key = Column(String(256), unique=True, nullable=False)
    user_email = Column(String(255))
    plan_type = Column(String(100))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)


class PendingTrade(Base):
    __tablename__ = "pending_trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    symbol = Column(String(20))
    trade_type = Column(String(10))  # BUY / SELL
    quantity = Column(Float)
    price = Column(Float)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100))
    message = Column(Text)
    level = Column(String(50), default="INFO")  # INFO / WARNING / ERROR
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ---------- Initialize Database ----------
def init_db():
    """
    Called once on app startup. Creates all tables on the active engine.
    Works for both Render PostgreSQL (via DB_URL) and local SQLite fallback.
    """
    try:
        print("🔹 Initializing database schema...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables ready.")
    except Exception as e:
        print("❌ Database initialization failed:", e)
        raise


# ---------- Entry Point ----------
if __name__ == "__main__":
    print("🔸 Running direct database initialization")
    init_db()