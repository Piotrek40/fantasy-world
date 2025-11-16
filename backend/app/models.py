"""SQLAlchemy models for Arkatar World Studio."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from .database import Base


class Location(Base):
    """Location model - cities, regions, kingdoms, etc."""
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)  # city, village, region, kingdom, continent, etc.
    parent_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    short_description = Column(String, nullable=True)
    long_description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)  # ["mountains", "port", "desert"]

    # Relationships
    parent_location = relationship("Location", remote_side=[id], backref="sub_locations")
    factions = relationship("Faction", back_populates="base_location")
    characters = relationship("Character", back_populates="home_location")


class Faction(Base):
    """Faction model - kingdoms, orders, guilds, cults, etc."""
    __tablename__ = "factions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)  # kingdom, order, guild, cult, clan, tribe
    base_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    ideology = Column(Text, nullable=True)
    goals = Column(Text, nullable=True)
    resources = Column(Float, default=0.0)
    power_level = Column(Float, default=0.0)

    # Relationships
    base_location = relationship("Location", back_populates="factions")
    members = relationship("Character", back_populates="faction")


class Character(Base):
    """Character model - people in the world."""
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)
    alias = Column(String, nullable=True)
    home_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    faction_id = Column(Integer, ForeignKey("factions.id"), nullable=True)
    role = Column(String, nullable=True)  # ruler, mage, assassin
    traits = Column(JSON, default=list)  # ["cruel", "loyal", "religious"]
    backstory = Column(Text, nullable=True)
    status = Column(String, default="alive")  # alive, missing, dead, unknown

    # Relationships
    home_location = relationship("Location", back_populates="characters")
    faction = relationship("Faction", back_populates="members")


class Religion(Base):
    """Religion/Deity model."""
    __tablename__ = "religions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)  # deity, cult, belief_system
    domains = Column(JSON, default=list)  # ["war", "sea", "death"]
    description = Column(Text, nullable=True)


class Item(Base):
    """Item/Artifact model."""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)  # weapon, artifact, mundane
    description = Column(Text, nullable=True)
    origin_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    # Relationships
    origin_location = relationship("Location")


class Relation(Base):
    """Relation between entities (characters, factions, locations)."""
    __tablename__ = "relations"

    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String, nullable=False)  # character, faction, location
    source_id = Column(Integer, nullable=False)
    target_type = Column(String, nullable=False)  # character, faction, location
    target_id = Column(Integer, nullable=False)
    relation_type = Column(String, nullable=False)  # alliance, hostility, vassalage, membership, dispute
    intensity = Column(Float, default=0.0)  # -100 (strong hostility) to 100 (strong alliance)
    notes = Column(Text, nullable=True)


class TimelineEvent(Base):
    """Historical event in the world timeline."""
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    date = Column(Integer, nullable=False, index=True)  # year
    era = Column(String, nullable=True)  # optional era name
    involved_locations = Column(JSON, default=list)  # list of location IDs
    involved_factions = Column(JSON, default=list)  # list of faction IDs
    involved_characters = Column(JSON, default=list)  # list of character IDs
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)  # ["war", "disaster", "uprising"]


class StoryArc(Base):
    """Story arc / quest / campaign."""
    __tablename__ = "story_arcs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    summary = Column(Text, nullable=True)
    main_conflict = Column(Text, nullable=True)
    key_characters = Column(JSON, default=list)  # list of character IDs
    key_locations = Column(JSON, default=list)  # list of location IDs
    related_events = Column(JSON, default=list)  # list of event IDs
    outline = Column(JSON, default=list)  # list of story beats: [{"step": 1, "description": "..."}]
    status = Column(String, default="draft")  # draft, in_progress, finished
