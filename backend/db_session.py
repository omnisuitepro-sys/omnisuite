# backend/db_session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Detect DB_URL (Render or other host)
db_url = os.getenv("DB_URL")

if not db_url:
    # Default to a writable temp directory inside the container
    os.makedirs("/tmp/data", exist_ok=True)
    db_path = os.path.join("/tmp/data", "omni_core.db")
    db_url = f"sqlite:///{db_path}"

engine = create_engine(
    db_url,
    echo=False,
    connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()