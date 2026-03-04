# app/routes/address.py
"""
FastAPI routes for Address operations.
Includes CRUD and search by distance.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
from app import crud, schemas
from app.database import get_db
from app.logging_config import logger

router = APIRouter(prefix="/addresses", tags=["Addresses"])

# -------------------------
# CREATE
# -------------------------
@router.post("/", response_model=schemas.AddressResponse)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    """
    Create a new address.
    """
    try:
        return crud.create_address(db, address)
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity Error: {e}")
        raise HTTPException(status_code=400, detail="Integrity constraint violation")
    except DataError as e:
        db.rollback()
        logger.error(f"Data Error: {e}")
        raise HTTPException(status_code=422, detail="Invalid data")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")


# -------------------------
# UPDATE
# -------------------------
@router.put("/{address_id}", response_model=schemas.AddressResponse)
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    """
    Update an existing address by ID.
    """
    try:
        updated = crud.update_address(db, address_id, address)
        if not updated:
            logger.warning(f"Address {address_id} not found for update")
            raise HTTPException(status_code=404, detail="Address not found")
        return updated
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity Error: {e}")
        raise HTTPException(status_code=400, detail="Integrity constraint violation")
    except DataError as e:
        db.rollback()
        logger.error(f"Data Error: {e}")
        raise HTTPException(status_code=422, detail="Invalid data")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")


# -------------------------
# DELETE
# -------------------------
@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    Delete an address by ID.
    """
    try:
        deleted = crud.delete_address(db, address_id)
        if not deleted:
            logger.warning(f"Address {address_id} not found for delete")
            raise HTTPException(status_code=404, detail="Address not found")
        logger.info(f"Address {address_id} deleted successfully")
        return {"message": "Deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")


# -------------------------
# SEARCH within distance
# -------------------------
@router.get("/search", response_model=list[schemas.AddressResponse])
def search_addresses(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    """
    Retrieve all addresses within a certain distance from given coordinates.
    """
    try:
        return crud.get_addresses_within_distance(db, latitude, longitude, distance_km)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB Error during search: {e}")
        raise HTTPException(status_code=500, detail="Database operation failed")
    
    
# -------------------------
# READ
# -------------------------
@router.get("/{address_id}", response_model=schemas.AddressResponse)
def read_address(address_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an address by ID.
    """
    address = crud.get_address(db, address_id)
    if not address:
        logger.warning(f"Address {address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    return address