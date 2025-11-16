"""API routes for Factions."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..crud import factions as crud

router = APIRouter(prefix="/factions", tags=["factions"])


@router.get("/", response_model=List[schemas.Faction])
def read_factions(
    skip: int = 0,
    limit: int = 100,
    faction_type: Optional[str] = Query(None, description="Filter by faction type"),
    search: Optional[str] = Query(None, description="Search in name, ideology, goals"),
    db: Session = Depends(get_db)
):
    """Get list of factions with optional filtering."""
    factions = crud.get_factions(
        db,
        skip=skip,
        limit=limit,
        faction_type=faction_type,
        search=search
    )
    return factions


@router.get("/{faction_id}", response_model=schemas.Faction)
def read_faction(faction_id: int, db: Session = Depends(get_db)):
    """Get a specific faction by ID."""
    faction = crud.get_faction(db, faction_id)
    if faction is None:
        raise HTTPException(status_code=404, detail="Faction not found")
    return faction


@router.post("/", response_model=schemas.Faction, status_code=201)
def create_faction(faction: schemas.FactionCreate, db: Session = Depends(get_db)):
    """Create a new faction."""
    return crud.create_faction(db, faction)


@router.put("/{faction_id}", response_model=schemas.Faction)
def update_faction(
    faction_id: int,
    faction: schemas.FactionUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing faction."""
    updated = crud.update_faction(db, faction_id, faction)
    if updated is None:
        raise HTTPException(status_code=404, detail="Faction not found")
    return updated


@router.delete("/{faction_id}", status_code=204)
def delete_faction(faction_id: int, db: Session = Depends(get_db)):
    """Delete a faction."""
    success = crud.delete_faction(db, faction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Faction not found")
    return None
