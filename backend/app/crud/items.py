"""CRUD operations for Items."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .. import models, schemas


def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    """Get a single item by ID."""
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    item_type: Optional[str] = None,
    search: Optional[str] = None
) -> List[models.Item]:
    """Get list of items with optional filtering."""
    query = db.query(models.Item)

    if item_type:
        query = query.filter(models.Item.type == item_type)

    if search:
        query = query.filter(
            or_(
                models.Item.name.contains(search),
                models.Item.description.contains(search)
            )
        )

    return query.offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    """Create a new item."""
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(
    db: Session,
    item_id: int,
    item: schemas.ItemUpdate
) -> Optional[models.Item]:
    """Update an existing item."""
    db_item = get_item(db, item_id)
    if not db_item:
        return None

    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> bool:
    """Delete an item."""
    db_item = get_item(db, item_id)
    if not db_item:
        return False

    db.delete(db_item)
    db.commit()
    return True
