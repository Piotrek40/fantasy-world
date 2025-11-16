"""API routes for Timeline Events."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..crud import timeline as crud

router = APIRouter(prefix="/timeline", tags=["timeline"])


@router.get("/", response_model=List[schemas.TimelineEvent])
def read_timeline_events(
    skip: int = 0,
    limit: int = 100,
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get timeline events ordered by date."""
    return crud.get_timeline_events(db, skip, limit, tags, search)


@router.get("/{event_id}", response_model=schemas.TimelineEvent)
def read_timeline_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific timeline event."""
    event = crud.get_timeline_event(db, event_id)
    if not event:
        raise HTTPException(404, "Event not found")
    return event


@router.post("/", response_model=schemas.TimelineEvent, status_code=201)
def create_timeline_event(event: schemas.TimelineEventCreate, db: Session = Depends(get_db)):
    """Create a new timeline event."""
    return crud.create_timeline_event(db, event)


@router.put("/{event_id}", response_model=schemas.TimelineEvent)
def update_timeline_event(event_id: int, event: schemas.TimelineEventUpdate, db: Session = Depends(get_db)):
    """Update a timeline event."""
    updated = crud.update_timeline_event(db, event_id, event)
    if not updated:
        raise HTTPException(404, "Event not found")
    return updated


@router.delete("/{event_id}", status_code=204)
def delete_timeline_event(event_id: int, db: Session = Depends(get_db)):
    """Delete a timeline event."""
    if not crud.delete_timeline_event(db, event_id):
        raise HTTPException(404, "Event not found")
