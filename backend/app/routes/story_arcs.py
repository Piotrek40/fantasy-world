"""API routes for Story Arcs."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..crud import story_arcs as crud

router = APIRouter(prefix="/story-arcs", tags=["story_arcs"])


@router.get("/", response_model=List[schemas.StoryArc])
def read_story_arcs(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of story arcs."""
    return crud.get_story_arcs(db, skip, limit, status)


@router.get("/{arc_id}", response_model=schemas.StoryArc)
def read_story_arc(arc_id: int, db: Session = Depends(get_db)):
    """Get a specific story arc."""
    arc = crud.get_story_arc(db, arc_id)
    if not arc:
        raise HTTPException(404, "Story arc not found")
    return arc


@router.post("/", response_model=schemas.StoryArc, status_code=201)
def create_story_arc(arc: schemas.StoryArcCreate, db: Session = Depends(get_db)):
    """Create a new story arc."""
    return crud.create_story_arc(db, arc)


@router.put("/{arc_id}", response_model=schemas.StoryArc)
def update_story_arc(arc_id: int, arc: schemas.StoryArcUpdate, db: Session = Depends(get_db)):
    """Update a story arc."""
    updated = crud.update_story_arc(db, arc_id, arc)
    if not updated:
        raise HTTPException(404, "Story arc not found")
    return updated


@router.delete("/{arc_id}", status_code=204)
def delete_story_arc(arc_id: int, db: Session = Depends(get_db)):
    """Delete a story arc."""
    if not crud.delete_story_arc(db, arc_id):
        raise HTTPException(404, "Story arc not found")
