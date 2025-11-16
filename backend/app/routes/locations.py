"""API routes for Locations."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..crud import locations as crud

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=List[schemas.Location])
def read_locations(
    skip: int = 0,
    limit: int = 100,
    location_type: Optional[str] = Query(None, description="Filter by location type"),
    search: Optional[str] = Query(None, description="Search in name and descriptions"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    db: Session = Depends(get_db)
):
    """Get list of locations with optional filtering."""
    locations = crud.get_locations(
        db,
        skip=skip,
        limit=limit,
        location_type=location_type,
        search=search,
        tags=tags
    )
    return locations


@router.get("/{location_id}", response_model=schemas.Location)
def read_location(location_id: int, db: Session = Depends(get_db)):
    """Get a specific location by ID."""
    location = crud.get_location(db, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/", response_model=schemas.Location, status_code=201)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    """Create a new location."""
    return crud.create_location(db, location)


@router.put("/{location_id}", response_model=schemas.Location)
def update_location(
    location_id: int,
    location: schemas.LocationUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing location."""
    updated = crud.update_location(db, location_id, location)
    if updated is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return updated


@router.delete("/{location_id}", status_code=204)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Delete a location."""
    success = crud.delete_location(db, location_id)
    if not success:
        raise HTTPException(status_code=404, detail="Location not found")
    return None
