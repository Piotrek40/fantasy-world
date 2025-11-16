#!/usr/bin/env python
"""
Arkatar World Studio CLI

Command-line interface for managing the fantasy world.
"""
import sys
import os
import argparse
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.database import Base
from backend.app import models
from backend.app.simulation import advance_history
from backend.app.export_markdown import export_world_to_markdown


# Database setup
DATABASE_URL = "sqlite:///./arkatar_world.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def list_characters(args):
    """List all characters."""
    db = SessionLocal()
    try:
        query = db.query(models.Character)

        if args.faction:
            query = query.filter(models.Character.faction_id == args.faction)

        characters = query.all()

        if not characters:
            print("No characters found.")
            return

        print(f"\n{'ID':<5} {'Name':<30} {'Faction':<20} {'Status':<10}")
        print("-" * 70)
        for char in characters:
            faction_name = ""
            if char.faction_id:
                faction = db.query(models.Faction).get(char.faction_id)
                faction_name = faction.name if faction else ""

            print(f"{char.id:<5} {char.name:<30} {faction_name:<20} {char.status:<10}")

        print(f"\nTotal: {len(characters)} characters")

    finally:
        db.close()


def list_factions(args):
    """List all factions and their relations."""
    db = SessionLocal()
    try:
        factions = db.query(models.Faction).all()

        if not factions:
            print("No factions found.")
            return

        for faction in factions:
            print(f"\n{'='*60}")
            print(f"Faction: {faction.name} ({faction.type})")
            print(f"Power Level: {faction.power_level}")
            print(f"Resources: {faction.resources}")

            # Get relations
            relations = db.query(models.Relation).filter(
                ((models.Relation.source_type == "faction") & (models.Relation.source_id == faction.id)) |
                ((models.Relation.target_type == "faction") & (models.Relation.target_id == faction.id))
            ).all()

            if relations:
                print("\nRelations:")
                for rel in relations:
                    other_id = rel.target_id if rel.source_id == faction.id else rel.source_id
                    other = db.query(models.Faction).get(other_id)
                    if other:
                        direction = "->" if rel.source_id == faction.id else "<-"
                        print(f"  {direction} {other.name}: {rel.relation_type} (intensity: {rel.intensity})")

        print(f"\n\nTotal: {len(factions)} factions")

    finally:
        db.close()


def export_markdown(args):
    """Export world to Markdown files."""
    db = SessionLocal()
    try:
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True, parents=True)

        print(f"Exporting world data to {output_dir}...")

        files = export_world_to_markdown(db)

        for filename, content in files.items():
            filepath = output_dir / filename
            filepath.write_text(content, encoding='utf-8')
            print(f"  Created: {filepath}")

        print(f"\nExport complete! {len(files)} files created.")

    finally:
        db.close()


def simulate(args):
    """Run history simulation."""
    db = SessionLocal()
    try:
        print(f"Running simulation for {args.ticks} ticks...")

        new_events, changed_relations = advance_history(db, args.ticks)

        print(f"\nSimulation complete!")
        print(f"  New events created: {len(new_events)}")
        print(f"  Relations changed: {len(changed_relations)}")

        if new_events:
            print("\nNew events:")
            for event in new_events:
                print(f"  - Year {event.date}: {event.title}")

        if args.verbose and changed_relations:
            print("\nRelation changes:")
            for change in changed_relations[:10]:  # Show first 10
                print(f"  Relation {change['relation_id']}: {change['old_intensity']:.1f} -> {change['new_intensity']:.1f}")

    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description="Arkatar World Studio CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # list-characters
    char_parser = subparsers.add_parser('list-characters', help='List all characters')
    char_parser.add_argument('--faction', type=int, help='Filter by faction ID')

    # list-factions
    faction_parser = subparsers.add_parser('list-factions', help='List all factions and their relations')

    # export-markdown
    export_parser = subparsers.add_parser('export-markdown', help='Export world to Markdown files')
    export_parser.add_argument('--output', required=True, help='Output directory')

    # simulate
    sim_parser = subparsers.add_parser('simulate', help='Run history simulation')
    sim_parser.add_argument('--ticks', type=int, required=True, help='Number of ticks to simulate')
    sim_parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Ensure database exists
    Base.metadata.create_all(engine)

    # Execute command
    commands = {
        'list-characters': list_characters,
        'list-factions': list_factions,
        'export-markdown': export_markdown,
        'simulate': simulate,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
