"""
Database Layer for GiriRaksha.
Supports both zero-setup local SQLite and production Supabase PostgreSQL.
"""

import os
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./giriraksha.db")

# For SQLite, ensure proper check_same_thread configuration
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(30), nullable=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    location_name = Column(String(255), default="Registered Location")
    radius_km = Column(Float, default=25.0)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CommunityReport(Base):
    __tablename__ = "community_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reporter_name = Column(String(100), default="Anonymous Mountain Commuter")
    contact = Column(String(100), nullable=True)
    hazard_type = Column(String(50), nullable=False) # Rockfall, Mudslide, Road Crack, Debris Flow
    severity = Column(String(30), default="Moderate") # Minor, Moderate, Critical
    description = Column(Text, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    location_name = Column(String(255), default="Unspecified Mountain Route")
    photo_url = Column(String(500), nullable=True)
    upvotes = Column(Integer, default=1)
    status = Column(String(30), default="VERIFIED_BY_COMMUNITY")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class OtpToken(Base):
    __tablename__ = "otp_tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), index=True, nullable=False)
    token_hash = Column(String(64), nullable=False) # SHA-256 hash
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ensure database tables exist immediately
init_db()
