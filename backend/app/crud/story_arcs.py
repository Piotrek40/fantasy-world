"""CRUD operations for Story Arcs."""
from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models, schemas


def get_story_arc(db: Session, arc_id: int) -> Optional[models.StoryArc]:
    return db.query(models.StoryArc).filter(models.StoryArc.id == arc_id).first()


def get_story_arcs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
) -> List[models.StoryArc]:
    query = db.query(models.StoryArc)

    if status:
        query = query.filter(models.StoryArc.status == status)

    return query.offset(skip).limit(limit).all()


def create_story_arc(db: Session, arc: schemas.StoryArcCreate) -> models.StoryArc:
    db_arc = models.StoryArc(**arc.model_dump())
    db.add(db_arc)
    db.commit()
    db.refresh(db_arc)
    return db_arc


def update_story_arc(
    db: Session, arc_id: int, arc: schemas.StoryArcUpdate
) -> Optional[models.StoryArc]:
    db_arc = get_story_arc(db, arc_id)
    if not db_arc:
        return None

    update_data = arc.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_arc, field, value)

    db.commit()
    db.refresh(db_arc)
    return db_arc


def delete_story_arc(db: Session, arc_id: int) -> bool:
    db_arc = get_story_arc(db, arc_id)
    if not db_arc:
        return False
    db.delete(db_arc)
    db.commit()
    return True
