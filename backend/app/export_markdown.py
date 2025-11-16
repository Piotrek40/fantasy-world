"""Export world data to Markdown format."""
from typing import Dict
from sqlalchemy.orm import Session

from . import models


def export_world_to_markdown(db: Session) -> Dict[str, str]:
    """
    Export entire world to Markdown files.

    Returns dict with filename: content pairs.
    """
    files = {}

    # World Overview
    locations = db.query(models.Location).all()
    factions = db.query(models.Faction).all()
    religions = db.query(models.Religion).all()

    overview = "# World Overview\n\n"
    overview += "## Locations\n\n"
    for loc in locations:
        overview += f"### {loc.name} ({loc.type})\n"
        if loc.short_description:
            overview += f"{loc.short_description}\n"
        if loc.tags:
            overview += f"**Tags:** {', '.join(loc.tags)}\n"
        overview += "\n"

    overview += "\n## Factions\n\n"
    for faction in factions:
        overview += f"### {faction.name} ({faction.type})\n"
        if faction.ideology:
            overview += f"**Ideology:** {faction.ideology}\n"
        if faction.goals:
            overview += f"**Goals:** {faction.goals}\n"
        overview += f"**Power Level:** {faction.power_level}\n\n"

    overview += "\n## Religions\n\n"
    for religion in religions:
        overview += f"### {religion.name} ({religion.type})\n"
        if religion.domains:
            overview += f"**Domains:** {', '.join(religion.domains)}\n"
        if religion.description:
            overview += f"{religion.description}\n"
        overview += "\n"

    files["world_overview.md"] = overview

    # Characters
    characters = db.query(models.Character).all()
    chars_md = "# Characters\n\n"
    for char in characters:
        chars_md += f"## {char.name}\n"
        if char.title:
            chars_md += f"**Title:** {char.title}\n"
        if char.role:
            chars_md += f"**Role:** {char.role}\n"
        if char.faction_id:
            faction = db.query(models.Faction).get(char.faction_id)
            if faction:
                chars_md += f"**Faction:** {faction.name}\n"
        if char.traits:
            chars_md += f"**Traits:** {', '.join(char.traits)}\n"
        if char.backstory:
            chars_md += f"\n{char.backstory}\n"
        chars_md += "\n---\n\n"

    files["characters.md"] = chars_md

    # Timeline
    events = db.query(models.TimelineEvent).order_by(models.TimelineEvent.date).all()
    timeline_md = "# Timeline\n\n"
    for event in events:
        timeline_md += f"## Year {event.date}: {event.title}\n"
        if event.era:
            timeline_md += f"*{event.era}*\n"
        if event.description:
            timeline_md += f"\n{event.description}\n"
        if event.tags:
            timeline_md += f"\n**Tags:** {', '.join(event.tags)}\n"
        timeline_md += "\n---\n\n"

    files["timeline.md"] = timeline_md

    # Story Arcs
    story_arcs = db.query(models.StoryArc).all()
    arcs_md = "# Story Arcs & Quests\n\n"
    for arc in story_arcs:
        arcs_md += f"## {arc.title}\n"
        arcs_md += f"**Status:** {arc.status}\n\n"
        if arc.summary:
            arcs_md += f"{arc.summary}\n\n"
        if arc.main_conflict:
            arcs_md += f"**Main Conflict:** {arc.main_conflict}\n\n"
        if arc.outline:
            arcs_md += "### Outline\n\n"
            for beat in arc.outline:
                arcs_md += f"{beat.get('step', '?')}. {beat.get('description', '')}\n"
            arcs_md += "\n"
        arcs_md += "---\n\n"

    files["story_arcs.md"] = arcs_md

    return files
