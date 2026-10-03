# backend/app/db/session.py
from sqlmodel import create_engine, Session
from app.core.config import settings
import socket

# ✅ Force IPv4
def force_ipv4():
    old_getaddrinfo = socket.getaddrinfo
    def new_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        return old_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
    socket.getaddrinfo = new_getaddrinfo

force_ipv4()

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

def get_db():
    with Session(engine) as session:
        yield session

def get_session():
    with Session(engine) as session:
        yield session