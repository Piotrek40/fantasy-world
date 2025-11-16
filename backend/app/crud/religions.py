"""CRUD operations for Religions."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .. import models, schemas


def get_religion(db: Session, religion_id: int) -> Optional[models.Religion]:
    """Get a single religion by ID."""
    return db.query(models.Religion).filter(models.Religion.id == religion_id).first()


def get_religions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    religion_type: Optional[str] = None,
    search: Optional[str] = None
) -> List[models.Religion]:
    """Get list of religions with optional filtering."""
    query = db.query(models.Religion)

    if religion_type:
        query = query.filter(models.Religion.type == religion_type)

    if search:
        query = query.filter(
            or_(
                models.Religion.name.contains(search),
                models.Religion.description.contains(search)
            )
        )

    return query.offset(skip).limit(limit).all()


def create_religion(db: Session, religion: schemas.ReligionCreate) -> models.Religion:
    """Create a new religion."""
    db_religion = models.Religion(**religion.model_dump())
    db.add(db_religion)
    db.commit()
    db.refresh(db_religion)
    return db_religion


def update_religion(
    db: Session,
    religion_id: int,
    religion: schemas.ReligionUpdate
) -> Optional[models.Religion]:
    """Update an existing religion."""
    db_religion = get_religion(db, religion_id)
    if not db_religion:
        return None

    update_data = religion.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_religion, field, value)

    db.commit()
    db.refresh(db_religion)
    return db_religion


def delete_religion(db: Session, religion_id: int) -> bool:
    """Delete a religion."""
    db_religion = get_religion(db, religion_id)
    if not db_religion:
        return False

    db.delete(db_religion)
    db.commit()
    return True
