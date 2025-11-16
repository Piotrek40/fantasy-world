"""Tests for Relations and Items API endpoints."""
import pytest


def test_items_crud(client):
    """Test basic CRUD operations for items."""
    # Create
    response = client.post(
        "/api/items/",
        json={
            "name": "Excalibur",
            "type": "artifact",
            "description": "The legendary sword"
        }
    )
    assert response.status_code == 201
    item_id = response.json()["id"]

    # Read
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Excalibur"

    # Update
    response = client.put(
        f"/api/items/{item_id}",
        json={"description": "Updated description"}
    )
    assert response.status_code == 200

    # List
    response = client.get("/api/items/")
    assert response.status_code == 200

    # Delete
    response = client.delete(f"/api/items/{item_id}")
    assert response.status_code == 204


def test_relations_crud(client):
    """Test basic CRUD operations for relations."""
    # Create two factions
    faction1 = client.post(
        "/api/factions/",
        json={"name": "Kingdom A", "type": "kingdom"}
    ).json()
    faction2 = client.post(
        "/api/factions/",
        json={"name": "Kingdom B", "type": "kingdom"}
    ).json()

    # Create relation
    response = client.post(
        "/api/relations/",
        json={
            "source_type": "faction",
            "source_id": faction1["id"],
            "target_type": "faction",
            "target_id": faction2["id"],
            "relation_type": "alliance",
            "intensity": 75.0,
            "notes": "Trade agreement"
        }
    )
    assert response.status_code == 201
    relation_id = response.json()["id"]

    # Read
    response = client.get(f"/api/relations/{relation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["relation_type"] == "alliance"
    assert data["intensity"] == 75.0

    # Update
    response = client.put(
        f"/api/relations/{relation_id}",
        json={"intensity": 50.0}
    )
    assert response.status_code == 200
    assert response.json()["intensity"] == 50.0

    # List
    response = client.get("/api/relations/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Delete
    response = client.delete(f"/api/relations/{relation_id}")
    assert response.status_code == 204


def test_entity_relations_endpoint(client):
    """Test getting all relations for a specific entity."""
    # Create entities
    faction1 = client.post(
        "/api/factions/",
        json={"name": "Empire X", "type": "kingdom"}
    ).json()
    faction2 = client.post(
        "/api/factions/",
        json={"name": "Republic Y", "type": "kingdom"}
    ).json()
    faction3 = client.post(
        "/api/factions/",
        json={"name": "Tribe Z", "type": "tribe"}
    ).json()

    # Create relations involving faction1
    client.post(
        "/api/relations/",
        json={
            "source_type": "faction",
            "source_id": faction1["id"],
            "target_type": "faction",
            "target_id": faction2["id"],
            "relation_type": "alliance",
            "intensity": 80.0
        }
    )
    client.post(
        "/api/relations/",
        json={
            "source_type": "faction",
            "source_id": faction3["id"],
            "target_type": "faction",
            "target_id": faction1["id"],
            "relation_type": "hostility",
            "intensity": -60.0
        }
    )

    # Get all relations for faction1
    response = client.get(f"/api/relations/entity/faction/{faction1['id']}")
    assert response.status_code == 200
    relations = response.json()
    assert len(relations) == 2


def test_filter_relations(client):
    """Test filtering relations by various criteria."""
    # Create entities
    char1 = client.post(
        "/api/characters/",
        json={"name": "Hero"}
    ).json()
    char2 = client.post(
        "/api/characters/",
        json={"name": "Villain"}
    ).json()

    # Create relation
    client.post(
        "/api/relations/",
        json={
            "source_type": "character",
            "source_id": char1["id"],
            "target_type": "character",
            "target_id": char2["id"],
            "relation_type": "rivalry",
            "intensity": -40.0
        }
    )

    # Filter by source_type
    response = client.get("/api/relations/?source_type=character")
    assert response.status_code == 200
    assert all(r["source_type"] == "character" for r in response.json())

    # Filter by relation_type
    response = client.get("/api/relations/?relation_type=rivalry")
    assert response.status_code == 200
    assert all(r["relation_type"] == "rivalry" for r in response.json())
