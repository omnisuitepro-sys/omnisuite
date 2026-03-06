import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Detect environment variable first (use Postgres if provided)
db_url = os.getenv("DB_URL")

if not db_url:
    # default to a writable SQLite path inside Render
    os.makedirs("/tmp/data", exist_ok=True)
    db_url = "sqlite:////tmp/data/omni_core.db"

engine = create_engine(
    db_url,
    echo=False,
    connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()