import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Detect database URL or fallback
DB_URL = os.getenv("DB_URL")

if not DB_URL:
    # Render runtime (Linux) path check
    if os.path.exists("/opt/render"):
        os.makedirs("/tmp/sqlite_data", exist_ok=True)
        DB_URL = "sqlite:////tmp/sqlite_data/omni_core.db"
    else:
        # Local Windows path for development
        DB_URL = "sqlite:///C:/OmniSuite/backend/omni_core.db"

engine = create_engine(
    DB_URL,
    echo=False,
    connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()