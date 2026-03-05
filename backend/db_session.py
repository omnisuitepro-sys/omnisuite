from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager  # only if needed elsewhere

# SQLite path  
db_url = "sqlite:///C:/OmniSuite/backend/omni_core.db"

engine = create_engine(
    db_url,
    echo=False,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# ✅ Correct version using `yield` – DO NOT wrap with @contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()