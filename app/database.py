from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from app.config import DB_PATH

DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True, nullable=False)
    room_type = Column(String, nullable=False)   # standard, deluxe, suite
    floor = Column(Integer)
    base_price = Column(Float, nullable=False)
    max_occupancy = Column(Integer, default=2)
    amenities = Column(Text)
    bookings = relationship("Booking", back_populates="room")


class Guest(Base):
    __tablename__ = "guests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    nationality = Column(String)
    phone = Column(String)
    loyalty_tier = Column(String, default="standard")  # standard, silver, gold
    total_stays = Column(Integer, default=0)
    bookings = relationship("Booking", back_populates="guest")


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey("guests.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    status = Column(String, default="confirmed")   # confirmed, checked_in, checked_out, cancelled
    total_amount = Column(Float)
    nightly_rate = Column(Float)
    num_guests = Column(Integer, default=1)
    special_requests = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    guest = relationship("Guest", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")


class Revenue(Base):
    __tablename__ = "revenue"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    room_revenue = Column(Float, default=0.0)
    food_revenue = Column(Float, default=0.0)
    spa_revenue = Column(Float, default=0.0)
    total_revenue = Column(Float, default=0.0)
    occupied_rooms = Column(Integer, default=0)
    total_rooms = Column(Integer, default=50)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
