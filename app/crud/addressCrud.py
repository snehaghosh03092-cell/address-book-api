# app/crud/address.py
"""
CRUD operations for Address model.
"""

from sqlalchemy.orm import Session
from app.models.address import Address
from app.schemas.addressSchema import AddressCreate, AddressUpdate
from geopy.distance import geodesic
from typing import List, Optional


# -------------------------
# CREATE
# -------------------------
def create_address(db: Session, address: AddressCreate) -> Address:
    """
    Create a new address in the database.
    
    Args:
        db (Session): Database session
        address (AddressCreate): Pydantic schema for new address
    
    Returns:
        Address: Newly created Address ORM object
    """
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)  # Load data from DB after commit
    return db_address


# -------------------------
# READ
# -------------------------
def get_address(db: Session, address_id: int) -> Optional[Address]:
    """
    Retrieve an address by ID.
    
    Args:
        db (Session): Database session
        address_id (int): ID of the address to fetch
    
    Returns:
        Optional[Address]: Address object or None if not found
    """
    return db.query(Address).filter(Address.id == address_id).first()


# -------------------------
# UPDATE
# -------------------------
def update_address(db: Session, address_id: int, address: AddressUpdate) -> Optional[Address]:
    """
    Update an existing address by ID.
    
    Args:
        db (Session): Database session
        address_id (int): ID of the address to update
        address (AddressUpdate): Pydantic schema with update data
    
    Returns:
        Optional[Address]: Updated Address object or None if not found
    """
    db_address = get_address(db, address_id)
    if not db_address:
        return None
    for key, val in address.dict().items():
        setattr(db_address, key, val)
    db.commit()
    db.refresh(db_address)
    return db_address


# -------------------------
# DELETE
# -------------------------
def delete_address(db: Session, address_id: int) -> Optional[Address]:
    """
    Delete an address by ID.
    
    Args:
        db (Session): Database session
        address_id (int): ID of the address to delete
    
    Returns:
        Optional[Address]: Deleted Address object or None if not found
    """
    db_address = get_address(db, address_id)
    if not db_address:
        return None
    db.delete(db_address)
    db.commit()
    return db_address


# -------------------------
# GET WITHIN DISTANCE
# -------------------------
def get_addresses_within_distance(
    db: Session, latitude: float, longitude: float, distance_km: float
) -> List[Address]:
    """
    Retrieve all addresses within a certain distance from given coordinates.
    
    Args:
        db (Session): Database session
        latitude (float): Latitude of the reference point
        longitude (float): Longitude of the reference point
        distance_km (float): Maximum distance in kilometers
    
    Returns:
        List[Address]: List of Address objects within the distance
    """
    addresses = db.query(Address).all()
    result = []
    for addr in addresses:
        if geodesic((addr.latitude, addr.longitude), (latitude, longitude)).km <= distance_km:
            result.append(addr)
    return result