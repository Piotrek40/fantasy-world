"""CRUD operations for Locations."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .. import models, schemas


def get_location(db: Session, location_id: int) -> Optional[models.Location]:
    """Get a single location by ID."""
    return db.query(models.Location).filter(models.Location.id == location_id).first()


def get_locations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    location_type: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> List[models.Location]:
    """Get list of locations with optional filtering."""
    query = db.query(models.Location)

    if location_type:
        query = query.filter(models.Location.type == location_type)

    if search:
        query = query.filter(
            or_(
                models.Location.name.contains(search),
                models.Location.short_description.contains(search),
                models.Location.long_description.contains(search)
            )
        )

    if tags:
        # Filter by tags - location must have at least one of the specified tags
        for tag in tags:
            query = query.filter(models.Location.tags.contains([tag]))

    return query.offset(skip).limit(limit).all()


def create_location(db: Session, location: schemas.LocationCreate) -> models.Location:
    """Create a new location."""
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def update_location(
    db: Session,
    location_id: int,
    location: schemas.LocationUpdate
) -> Optional[models.Location]:
    """Update an existing location."""
    db_location = get_location(db, location_id)
    if not db_location:
        return None

    update_data = location.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_location, field, value)

    db.commit()
    db.refresh(db_location)
    return db_location


def delete_location(db: Session, location_id: int) -> bool:
    """Delete a location."""
    db_location = get_location(db, location_id)
    if not db_location:
        return False

    db.delete(db_location)
    db.commit()
    return True
