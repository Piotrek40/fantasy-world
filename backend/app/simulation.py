"""History simulation engine."""
import random
from typing import List, Tuple
from sqlalchemy.orm import Session

from . import models


def advance_history(db: Session, ticks: int) -> Tuple[List[models.TimelineEvent], List[dict]]:
    """
    Advance world history by specified number of ticks.

    Returns:
        - List of newly created TimelineEvents
        - List of changed relations (before/after)
    """
    new_events = []
    changed_relations = []

    # Get all factions and relations
    factions = db.query(models.Faction).all()
    relations = db.query(models.Relation).filter(
        models.Relation.source_type == "faction",
        models.Relation.target_type == "faction"
    ).all()

    # Current year (max date from timeline or 0)
    max_date_result = db.query(models.TimelineEvent).order_by(
        models.TimelineEvent.date.desc()
    ).first()
    current_year = max_date_result.date if max_date_result else 1000

    for tick in range(ticks):
        current_year += 1

        # Update relations based on simple rules
        for relation in relations:
            old_intensity = relation.intensity

            # Random drift
            drift = random.uniform(-5, 5)

            # Tendency towards conflict or peace based on current state
            if relation.intensity < -30:
                # Hostile relations tend to escalate
                drift += random.uniform(-10, 5)
            elif relation.intensity > 30:
                # Friendly relations tend to strengthen
                drift += random.uniform(-5, 10)

            relation.intensity = max(-100, min(100, relation.intensity + drift))

            # Record significant changes
            if abs(relation.intensity - old_intensity) > 10:
                changed_relations.append({
                    "relation_id": relation.id,
                    "source_id": relation.source_id,
                    "target_id": relation.target_id,
                    "old_intensity": round(old_intensity, 2),
                    "new_intensity": round(relation.intensity, 2)
                })

        # Create events for major relation changes
        for change in changed_relations[-len(relations):]:  # Only recent changes this tick
            if abs(change["new_intensity"] - change["old_intensity"]) > 20:
                event_type = "conflict" if change["new_intensity"] < -50 else "treaty" if change["new_intensity"] > 50 else "tension"

                event = models.TimelineEvent(
                    title=f"{'War' if event_type == 'conflict' else 'Alliance' if event_type == 'treaty' else 'Diplomatic Tension'}",
                    date=current_year,
                    involved_factions=[change["source_id"], change["target_id"]],
                    description=f"Relations changed from {change['old_intensity']:.0f} to {change['new_intensity']:.0f}",
                    tags=[event_type]
                )
                db.add(event)
                new_events.append(event)

    db.commit()

    # Refresh all new events to get IDs
    for event in new_events:
        db.refresh(event)

    return new_events, changed_relations
