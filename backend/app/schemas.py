"""Pydantic schemas for API requests/responses."""
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# Location Schemas
class LocationBase(BaseModel):
    name: str
    type: str
    parent_location_id: Optional[int] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    tags: List[str] = []


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    parent_location_id: Optional[int] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    tags: Optional[List[str]] = None


class Location(LocationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Faction Schemas
class FactionBase(BaseModel):
    name: str
    type: str
    base_location_id: Optional[int] = None
    ideology: Optional[str] = None
    goals: Optional[str] = None
    resources: float = 0.0
    power_level: float = 0.0


class FactionCreate(FactionBase):
    pass


class FactionUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    base_location_id: Optional[int] = None
    ideology: Optional[str] = None
    goals: Optional[str] = None
    resources: Optional[float] = None
    power_level: Optional[float] = None


class Faction(FactionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Character Schemas
class CharacterBase(BaseModel):
    name: str
    title: Optional[str] = None
    alias: Optional[str] = None
    home_location_id: Optional[int] = None
    faction_id: Optional[int] = None
    role: Optional[str] = None
    traits: List[str] = []
    backstory: Optional[str] = None
    status: str = "alive"


class CharacterCreate(CharacterBase):
    pass


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    alias: Optional[str] = None
    home_location_id: Optional[int] = None
    faction_id: Optional[int] = None
    role: Optional[str] = None
    traits: Optional[List[str]] = None
    backstory: Optional[str] = None
    status: Optional[str] = None


class Character(CharacterBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Religion Schemas
class ReligionBase(BaseModel):
    name: str
    type: str
    domains: List[str] = []
    description: Optional[str] = None


class ReligionCreate(ReligionBase):
    pass


class ReligionUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    domains: Optional[List[str]] = None
    description: Optional[str] = None


class Religion(ReligionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Item Schemas
class ItemBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    origin_location_id: Optional[int] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    origin_location_id: Optional[int] = None


class Item(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Relation Schemas
class RelationBase(BaseModel):
    source_type: str
    source_id: int
    target_type: str
    target_id: int
    relation_type: str
    intensity: float = 0.0
    notes: Optional[str] = None


class RelationCreate(RelationBase):
    pass


class RelationUpdate(BaseModel):
    relation_type: Optional[str] = None
    intensity: Optional[float] = None
    notes: Optional[str] = None


class Relation(RelationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# TimelineEvent Schemas
class TimelineEventBase(BaseModel):
    title: str
    date: int
    era: Optional[str] = None
    involved_locations: List[int] = []
    involved_factions: List[int] = []
    involved_characters: List[int] = []
    description: Optional[str] = None
    tags: List[str] = []


class TimelineEventCreate(TimelineEventBase):
    pass


class TimelineEventUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[int] = None
    era: Optional[str] = None
    involved_locations: Optional[List[int]] = None
    involved_factions: Optional[List[int]] = None
    involved_characters: Optional[List[int]] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class TimelineEvent(TimelineEventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# StoryArc Schemas
class StoryBeat(BaseModel):
    step: int
    description: str


class StoryArcBase(BaseModel):
    title: str
    summary: Optional[str] = None
    main_conflict: Optional[str] = None
    key_characters: List[int] = []
    key_locations: List[int] = []
    related_events: List[int] = []
    outline: List[StoryBeat] = []
    status: str = "draft"


class StoryArcCreate(StoryArcBase):
    pass


class StoryArcUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    main_conflict: Optional[str] = None
    key_characters: Optional[List[int]] = None
    key_locations: Optional[List[int]] = None
    related_events: Optional[List[int]] = None
    outline: Optional[List[StoryBeat]] = None
    status: Optional[str] = None


class StoryArc(StoryArcBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# World Snapshot Schema
class WorldSnapshot(BaseModel):
    locations: List[Location]
    factions: List[Faction]
    characters: List[Character]
    religions: List[Religion]
    items: List[Item]
    relations: List[Relation]
    timeline_events: List[TimelineEvent]
    story_arcs: List[StoryArc]


# Simulation Result Schema
class SimulationResult(BaseModel):
    ticks_advanced: int
    new_events: List[TimelineEvent]
    changed_relations: List[dict]  # {"relation_id": int, "old_intensity": float, "new_intensity": float}
