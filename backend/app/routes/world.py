"""API routes for world operations (snapshot, simulation, export)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db
from ..simulation import advance_history
from ..export_markdown import export_world_to_markdown
from ..crud import (
    locations, factions, characters, religions, items,
    relations, timeline, story_arcs
)

router = APIRouter(prefix="/world", tags=["world"])


@router.get("/snapshot", response_model=schemas.WorldSnapshot)
def get_world_snapshot(db: Session = Depends(get_db)):
    """Get complete snapshot of the world."""
    return schemas.WorldSnapshot(
        locations=[schemas.Location.model_validate(l) for l in db.query(models.Location).all()],
        factions=[schemas.Faction.model_validate(f) for f in db.query(models.Faction).all()],
        characters=[schemas.Character.model_validate(c) for c in db.query(models.Character).all()],
        religions=[schemas.Religion.model_validate(r) for r in db.query(models.Religion).all()],
        items=[schemas.Item.model_validate(i) for i in db.query(models.Item).all()],
        relations=[schemas.Relation.model_validate(r) for r in db.query(models.Relation).all()],
        timeline_events=[schemas.TimelineEvent.model_validate(e) for e in db.query(models.TimelineEvent).all()],
        story_arcs=[schemas.StoryArc.model_validate(a) for a in db.query(models.StoryArc).all()]
    )


@router.post("/simulate", response_model=schemas.SimulationResult)
def simulate_history(ticks: int, db: Session = Depends(get_db)):
    """Advance history simulation by specified ticks."""
    new_events, changed_relations = advance_history(db, ticks)

    return schemas.SimulationResult(
        ticks_advanced=ticks,
        new_events=[schemas.TimelineEvent.model_validate(e) for e in new_events],
        changed_relations=changed_relations
    )


@router.get("/export/markdown")
def export_markdown(db: Session = Depends(get_db)):
    """Export world data to Markdown format."""
    return export_world_to_markdown(db)
