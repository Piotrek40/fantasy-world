"""CRUD operations for Factions."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .. import models, schemas


def get_faction(db: Session, faction_id: int) -> Optional[models.Faction]:
    """Get a single faction by ID."""
    return db.query(models.Faction).filter(models.Faction.id == faction_id).first()


def get_factions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    faction_type: Optional[str] = None,
    search: Optional[str] = None
) -> List[models.Faction]:
    """Get list of factions with optional filtering."""
    query = db.query(models.Faction)

    if faction_type:
        query = query.filter(models.Faction.type == faction_type)

    if search:
        query = query.filter(
            or_(
                models.Faction.name.contains(search),
                models.Faction.ideology.contains(search),
                models.Faction.goals.contains(search)
            )
        )

    return query.offset(skip).limit(limit).all()


def create_faction(db: Session, faction: schemas.FactionCreate) -> models.Faction:
    """Create a new faction."""
    db_faction = models.Faction(**faction.model_dump())
    db.add(db_faction)
    db.commit()
    db.refresh(db_faction)
    return db_faction


def update_faction(
    db: Session,
    faction_id: int,
    faction: schemas.FactionUpdate
) -> Optional[models.Faction]:
    """Update an existing faction."""
    db_faction = get_faction(db, faction_id)
    if not db_faction:
        return None

    update_data = faction.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_faction, field, value)

    db.commit()
    db.refresh(db_faction)
    return db_faction


def delete_faction(db: Session, faction_id: int) -> bool:
    """Delete a faction."""
    db_faction = get_faction(db, faction_id)
    if not db_faction:
        return False

    db.delete(db_faction)
    db.commit()
    return True
