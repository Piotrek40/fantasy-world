"""CRUD operations for Timeline Events."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .. import models, schemas


def get_timeline_event(db: Session, event_id: int) -> Optional[models.TimelineEvent]:
    return db.query(models.TimelineEvent).filter(models.TimelineEvent.id == event_id).first()


def get_timeline_events(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None,
    order_by_date: bool = True
) -> List[models.TimelineEvent]:
    query = db.query(models.TimelineEvent)

    if search:
        query = query.filter(
            or_(
                models.TimelineEvent.title.contains(search),
                models.TimelineEvent.description.contains(search)
            )
        )

    if tags:
        for tag in tags:
            query = query.filter(models.TimelineEvent.tags.contains([tag]))

    if order_by_date:
        query = query.order_by(models.TimelineEvent.date.asc())

    return query.offset(skip).limit(limit).all()


def create_timeline_event(db: Session, event: schemas.TimelineEventCreate) -> models.TimelineEvent:
    db_event = models.TimelineEvent(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_timeline_event(
    db: Session, event_id: int, event: schemas.TimelineEventUpdate
) -> Optional[models.TimelineEvent]:
    db_event = get_timeline_event(db, event_id)
    if not db_event:
        return None

    update_data = event.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)

    db.commit()
    db.refresh(db_event)
    return db_event


def delete_timeline_event(db: Session, event_id: int) -> bool:
    db_event = get_timeline_event(db, event_id)
    if not db_event:
        return False
    db.delete(db_event)
    db.commit()
    return True
