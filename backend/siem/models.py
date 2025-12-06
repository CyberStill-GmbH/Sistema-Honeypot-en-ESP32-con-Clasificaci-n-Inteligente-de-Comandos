from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Text,
    Boolean,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from .config_siem import DATABASE_URI

# ---------------------------------------------------------------------
# BASE Y ENGINE
# ---------------------------------------------------------------------
Base = declarative_base()
engine = create_engine(DATABASE_URI, echo=False, future=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

# ---------------------------------------------------------------------
# MODELOS
# ---------------------------------------------------------------------

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class ApiToken(Base):
    __tablename__ = "api_tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String(128), unique=True, nullable=False, index=True)
    owner = Column(String(64), nullable=True, default="default")
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    source_ip = Column(String(64))
    raw_cmd = Column(Text)
    label = Column(String(32))
    score = Column(Float)
    reason = Column(Text)
    extra = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "source_ip": self.source_ip,
            "raw_cmd": self.raw_cmd,
            "label": self.label,
            "score": self.score,
            "reason": self.reason,
            "extra": self.extra,
        }


# ---------------------------------------------------------------------
# INIT DB
# ---------------------------------------------------------------------
def init_db():
    global engine
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)