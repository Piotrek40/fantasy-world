"""API routes for Characters."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..crud import characters as crud

router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("/", response_model=List[schemas.Character])
def read_characters(
    skip: int = 0,
    limit: int = 100,
    faction_id: Optional[int] = Query(None, description="Filter by faction ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in name, title, alias, backstory"),
    db: Session = Depends(get_db)
):
    """Get list of characters with optional filtering."""
    characters = crud.get_characters(
        db,
        skip=skip,
        limit=limit,
        faction_id=faction_id,
        status=status,
        search=search
    )
    return characters


@router.get("/{character_id}", response_model=schemas.Character)
def read_character(character_id: int, db: Session = Depends(get_db)):
    """Get a specific character by ID."""
    character = crud.get_character(db, character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.post("/", response_model=schemas.Character, status_code=201)
def create_character(character: schemas.CharacterCreate, db: Session = Depends(get_db)):
    """Create a new character."""
    return crud.create_character(db, character)


@router.put("/{character_id}", response_model=schemas.Character)
def update_character(
    character_id: int,
    character: schemas.CharacterUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing character."""
    updated = crud.update_character(db, character_id, character)
    if updated is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return updated


@router.delete("/{character_id}", status_code=204)
def delete_character(character_id: int, db: Session = Depends(get_db)):
    """Delete a character."""
    success = crud.delete_character(db, character_id)
    if not success:
        raise HTTPException(status_code=404, detail="Character not found")
    return None
