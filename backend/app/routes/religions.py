"""API routes for Religions."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..crud import religions as crud

router = APIRouter(prefix="/religions", tags=["religions"])


@router.get("/", response_model=List[schemas.Religion])
def read_religions(
    skip: int = 0,
    limit: int = 100,
    religion_type: Optional[str] = Query(None, description="Filter by religion type"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    db: Session = Depends(get_db)
):
    """Get list of religions with optional filtering."""
    religions = crud.get_religions(
        db,
        skip=skip,
        limit=limit,
        religion_type=religion_type,
        search=search
    )
    return religions


@router.get("/{religion_id}", response_model=schemas.Religion)
def read_religion(religion_id: int, db: Session = Depends(get_db)):
    """Get a specific religion by ID."""
    religion = crud.get_religion(db, religion_id)
    if religion is None:
        raise HTTPException(status_code=404, detail="Religion not found")
    return religion


@router.post("/", response_model=schemas.Religion, status_code=201)
def create_religion(religion: schemas.ReligionCreate, db: Session = Depends(get_db)):
    """Create a new religion."""
    return crud.create_religion(db, religion)


@router.put("/{religion_id}", response_model=schemas.Religion)
def update_religion(
    religion_id: int,
    religion: schemas.ReligionUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing religion."""
    updated = crud.update_religion(db, religion_id, religion)
    if updated is None:
        raise HTTPException(status_code=404, detail="Religion not found")
    return updated


@router.delete("/{religion_id}", status_code=204)
def delete_religion(religion_id: int, db: Session = Depends(get_db)):
    """Delete a religion."""
    success = crud.delete_religion(db, religion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Religion not found")
    return None
