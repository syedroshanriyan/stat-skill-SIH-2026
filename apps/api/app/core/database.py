import os
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

# Engine configuration
connect_args = {}
db_url = settings.DATABASE_URL

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    if db_url.startswith("sqlite:///./"):
        db_name = db_url.replace("sqlite:///./", "")
        # Look in current cwd first, then check workspace root
        cwd_db = Path.cwd() / db_name
        root_db = Path(__file__).resolve().parents[3] / db_name
        if not cwd_db.exists() and root_db.exists():
            db_url = f"sqlite:///{root_db.as_posix()}"
        elif cwd_db.exists():
            db_url = f"sqlite:///{cwd_db.as_posix()}"

engine = create_engine(
    db_url,
    echo=False,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
