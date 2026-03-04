# app/models/address.py
"""
SQLAlchemy model for the Address entity.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database import Base

class Address(Base):
    """
    Represents an address record in the database.
    
    Attributes:
        id (int): Primary key
        name (str): Name of the person or entity
        street (str): Street name
        city (str): City name
        latitude (float): Latitude coordinate (-90 to 90)
        longitude (float): Longitude coordinate (-180 to 180)
        created_at (datetime): UTC timestamp when the record was created
    """
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    street = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)