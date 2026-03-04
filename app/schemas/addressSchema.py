# app/schemas/address.py
"""
Pydantic schemas for Address API.
Defines request and response models for CRUD operations.
"""

from pydantic import BaseModel, Field, field_validator

class AddressBase(BaseModel):
    """
    Base schema shared by create/update operations.
    """
    name: str = Field(..., max_length=100)
    street: str = Field(..., min_length=3)
    city: str = Field(..., min_length=2)
    latitude: float
    longitude: float

    # -------------------------
    # Field validators
    # -------------------------
    @field_validator("latitude")
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return v


class AddressCreate(AddressBase):
    """Schema for creating a new address"""
    pass


class AddressUpdate(AddressBase):
    """Schema for updating an existing address"""
    pass


class AddressResponse(AddressBase):
    """Schema for returning address data to clients"""
    id: int

    class Config:
        orm_mode = True