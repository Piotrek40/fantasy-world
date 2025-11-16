"""CRUD operations for Characters."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .. import models, schemas


def get_character(db: Session, character_id: int) -> Optional[models.Character]:
    """Get a single character by ID."""
    return db.query(models.Character).filter(models.Character.id == character_id).first()


def get_characters(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    faction_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> List[models.Character]:
    """Get list of characters with optional filtering."""
    query = db.query(models.Character)

    if faction_id:
        query = query.filter(models.Character.faction_id == faction_id)

    if status:
        query = query.filter(models.Character.status == status)

    if search:
        query = query.filter(
            or_(
                models.Character.name.contains(search),
                models.Character.title.contains(search),
                models.Character.alias.contains(search),
                models.Character.backstory.contains(search)
            )
        )

    return query.offset(skip).limit(limit).all()


def create_character(db: Session, character: schemas.CharacterCreate) -> models.Character:
    """Create a new character."""
    db_character = models.Character(**character.model_dump())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character


def update_character(
    db: Session,
    character_id: int,
    character: schemas.CharacterUpdate
) -> Optional[models.Character]:
    """Update an existing character."""
    db_character = get_character(db, character_id)
    if not db_character:
        return None

    update_data = character.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_character, field, value)

    db.commit()
    db.refresh(db_character)
    return db_character


def delete_character(db: Session, character_id: int) -> bool:
    """Delete a character."""
    db_character = get_character(db, character_id)
    if not db_character:
        return False

    db.delete(db_character)
    db.commit()
    return True
