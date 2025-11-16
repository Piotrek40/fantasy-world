"""CRUD operations for Relations."""
from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models, schemas


def get_relation(db: Session, relation_id: int) -> Optional[models.Relation]:
    """Get a single relation by ID."""
    return db.query(models.Relation).filter(models.Relation.id == relation_id).first()


def get_relations(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    source_type: Optional[str] = None,
    source_id: Optional[int] = None,
    target_type: Optional[str] = None,
    target_id: Optional[int] = None,
    relation_type: Optional[str] = None
) -> List[models.Relation]:
    """Get list of relations with optional filtering."""
    query = db.query(models.Relation)

    if source_type:
        query = query.filter(models.Relation.source_type == source_type)

    if source_id:
        query = query.filter(models.Relation.source_id == source_id)

    if target_type:
        query = query.filter(models.Relation.target_type == target_type)

    if target_id:
        query = query.filter(models.Relation.target_id == target_id)

    if relation_type:
        query = query.filter(models.Relation.relation_type == relation_type)

    return query.offset(skip).limit(limit).all()


def get_entity_relations(
    db: Session,
    entity_type: str,
    entity_id: int
) -> List[models.Relation]:
    """Get all relations for a specific entity (as source or target)."""
    return db.query(models.Relation).filter(
        ((models.Relation.source_type == entity_type) & (models.Relation.source_id == entity_id)) |
        ((models.Relation.target_type == entity_type) & (models.Relation.target_id == entity_id))
    ).all()


def create_relation(db: Session, relation: schemas.RelationCreate) -> models.Relation:
    """Create a new relation."""
    db_relation = models.Relation(**relation.model_dump())
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation


def update_relation(
    db: Session,
    relation_id: int,
    relation: schemas.RelationUpdate
) -> Optional[models.Relation]:
    """Update an existing relation."""
    db_relation = get_relation(db, relation_id)
    if not db_relation:
        return None

    update_data = relation.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_relation, field, value)

    db.commit()
    db.refresh(db_relation)
    return db_relation


def delete_relation(db: Session, relation_id: int) -> bool:
    """Delete a relation."""
    db_relation = get_relation(db, relation_id)
    if not db_relation:
        return False

    db.delete(db_relation)
    db.commit()
    return True
