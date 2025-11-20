from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def init_pgvector():
    # Try to ensure pgvector extension exists; requires superuser privileges
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS vector")
    except Exception:
        # Ignore if extension cannot be created; database may be managed externally
        pass
