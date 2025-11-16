"""Tests for database models."""
import pytest
from app import models


def test_create_location(db_session):
    """Test creating a location."""
    location = models.Location(
        name="Silverhold",
        type="city",
        short_description="A bustling port city",
        tags=["port", "trade", "coastal"]
    )
    db_session.add(location)
    db_session.commit()
    db_session.refresh(location)

    assert location.id is not None
    assert location.name == "Silverhold"
    assert location.type == "city"
    assert "port" in location.tags


def test_location_hierarchy(db_session):
    """Test location parent-child relationships."""
    kingdom = models.Location(
        name="Northern Kingdoms",
        type="kingdom"
    )
    db_session.add(kingdom)
    db_session.commit()

    city = models.Location(
        name="Frostpeak",
        type="city",
        parent_location_id=kingdom.id
    )
    db_session.add(city)
    db_session.commit()
    db_session.refresh(kingdom)

    assert city.parent_location.name == "Northern Kingdoms"
    assert len(kingdom.sub_locations) == 1
    assert kingdom.sub_locations[0].name == "Frostpeak"


def test_create_faction(db_session):
    """Test creating a faction."""
    location = models.Location(name="Capital", type="city")
    db_session.add(location)
    db_session.commit()

    faction = models.Faction(
        name="Royal Guard",
        type="order",
        base_location_id=location.id,
        ideology="Protect the realm",
        resources=1000.0,
        power_level=75.0
    )
    db_session.add(faction)
    db_session.commit()
    db_session.refresh(faction)

    assert faction.id is not None
    assert faction.name == "Royal Guard"
    assert faction.base_location.name == "Capital"


def test_create_character(db_session):
    """Test creating a character."""
    location = models.Location(name="Village", type="village")
    faction = models.Faction(name="Farmers Guild", type="guild")
    db_session.add_all([location, faction])
    db_session.commit()

    character = models.Character(
        name="Aldric",
        title="The Brave",
        home_location_id=location.id,
        faction_id=faction.id,
        role="warrior",
        traits=["brave", "loyal"],
        backstory="A simple farmer turned hero",
        status="alive"
    )
    db_session.add(character)
    db_session.commit()
    db_session.refresh(character)

    assert character.id is not None
    assert character.name == "Aldric"
    assert character.home_location.name == "Village"
    assert character.faction.name == "Farmers Guild"
    assert "brave" in character.traits


def test_character_faction_relationship(db_session):
    """Test character-faction relationship."""
    faction = models.Faction(name="Mages Circle", type="guild")
    db_session.add(faction)
    db_session.commit()

    char1 = models.Character(name="Merlin", faction_id=faction.id)
    char2 = models.Character(name="Gandor", faction_id=faction.id)
    db_session.add_all([char1, char2])
    db_session.commit()
    db_session.refresh(faction)

    assert len(faction.members) == 2
    assert {m.name for m in faction.members} == {"Merlin", "Gandor"}


def test_create_religion(db_session):
    """Test creating a religion."""
    religion = models.Religion(
        name="Order of Light",
        type="deity",
        domains=["light", "justice", "healing"],
        description="Worship of the Sun God"
    )
    db_session.add(religion)
    db_session.commit()
    db_session.refresh(religion)

    assert religion.id is not None
    assert religion.name == "Order of Light"
    assert "justice" in religion.domains


def test_create_item(db_session):
    """Test creating an item."""
    location = models.Location(name="Ancient Ruins", type="ruins")
    db_session.add(location)
    db_session.commit()

    item = models.Item(
        name="Sword of Dawn",
        type="artifact",
        description="A legendary blade",
        origin_location_id=location.id
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)

    assert item.id is not None
    assert item.name == "Sword of Dawn"
    assert item.origin_location.name == "Ancient Ruins"


def test_create_relation(db_session):
    """Test creating a relation between entities."""
    faction1 = models.Faction(name="Kingdom A", type="kingdom")
    faction2 = models.Faction(name="Kingdom B", type="kingdom")
    db_session.add_all([faction1, faction2])
    db_session.commit()

    relation = models.Relation(
        source_type="faction",
        source_id=faction1.id,
        target_type="faction",
        target_id=faction2.id,
        relation_type="alliance",
        intensity=80.0,
        notes="Trade agreement"
    )
    db_session.add(relation)
    db_session.commit()
    db_session.refresh(relation)

    assert relation.id is not None
    assert relation.relation_type == "alliance"
    assert relation.intensity == 80.0


def test_create_timeline_event(db_session):
    """Test creating a timeline event."""
    location = models.Location(name="Battlefield", type="plain")
    faction = models.Faction(name="Empire", type="kingdom")
    character = models.Character(name="General Marcus")
    db_session.add_all([location, faction, character])
    db_session.commit()

    event = models.TimelineEvent(
        title="Battle of Red Plains",
        date=1205,
        era="Age of Conflict",
        involved_locations=[location.id],
        involved_factions=[faction.id],
        involved_characters=[character.id],
        description="A major battle",
        tags=["war", "battle"]
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    assert event.id is not None
    assert event.title == "Battle of Red Plains"
    assert event.date == 1205
    assert location.id in event.involved_locations
    assert "war" in event.tags


def test_create_story_arc(db_session):
    """Test creating a story arc."""
    character = models.Character(name="Hero")
    location = models.Location(name="Quest Location", type="dungeon")
    event = models.TimelineEvent(title="Quest Start", date=1300)
    db_session.add_all([character, location, event])
    db_session.commit()

    story_arc = models.StoryArc(
        title="The Hero's Journey",
        summary="An epic quest",
        main_conflict="Defeat the evil lord",
        key_characters=[character.id],
        key_locations=[location.id],
        related_events=[event.id],
        outline=[
            {"step": 1, "description": "Hero accepts the quest"},
            {"step": 2, "description": "Journey to the dungeon"},
            {"step": 3, "description": "Final confrontation"}
        ],
        status="draft"
    )
    db_session.add(story_arc)
    db_session.commit()
    db_session.refresh(story_arc)

    assert story_arc.id is not None
    assert story_arc.title == "The Hero's Journey"
    assert len(story_arc.outline) == 3
    assert story_arc.outline[0]["step"] == 1
