"""API routes for Relations."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..crud import relations as crud

router = APIRouter(prefix="/relations", tags=["relations"])


@router.get("/", response_model=List[schemas.Relation])
def read_relations(
    skip: int = 0,
    limit: int = 100,
    source_type: Optional[str] = Query(None, description="Filter by source entity type"),
    source_id: Optional[int] = Query(None, description="Filter by source entity ID"),
    target_type: Optional[str] = Query(None, description="Filter by target entity type"),
    target_id: Optional[int] = Query(None, description="Filter by target entity ID"),
    relation_type: Optional[str] = Query(None, description="Filter by relation type"),
    db: Session = Depends(get_db)
):
    """Get list of relations with optional filtering."""
    relations = crud.get_relations(
        db,
        skip=skip,
        limit=limit,
        source_type=source_type,
        source_id=source_id,
        target_type=target_type,
        target_id=target_id,
        relation_type=relation_type
    )
    return relations


@router.get("/entity/{entity_type}/{entity_id}", response_model=List[schemas.Relation])
def read_entity_relations(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db)
):
    """Get all relations for a specific entity."""
    relations = crud.get_entity_relations(db, entity_type, entity_id)
    return relations


@router.get("/{relation_id}", response_model=schemas.Relation)
def read_relation(relation_id: int, db: Session = Depends(get_db)):
    """Get a specific relation by ID."""
    relation = crud.get_relation(db, relation_id)
    if relation is None:
        raise HTTPException(status_code=404, detail="Relation not found")
    return relation


@router.post("/", response_model=schemas.Relation, status_code=201)
def create_relation(relation: schemas.RelationCreate, db: Session = Depends(get_db)):
    """Create a new relation."""
    return crud.create_relation(db, relation)


@router.put("/{relation_id}", response_model=schemas.Relation)
def update_relation(
    relation_id: int,
    relation: schemas.RelationUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing relation."""
    updated = crud.update_relation(db, relation_id, relation)
    if updated is None:
        raise HTTPException(status_code=404, detail="Relation not found")
    return updated


@router.delete("/{relation_id}", status_code=204)
def delete_relation(relation_id: int, db: Session = Depends(get_db)):
    """Delete a relation."""
    success = crud.delete_relation(db, relation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Relation not found")
    return None
