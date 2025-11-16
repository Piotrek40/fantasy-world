"""Basic API tests for all entity types."""
import pytest


def test_factions_crud(client):
    """Test basic CRUD operations for factions."""
    # Create
    response = client.post(
        "/api/factions/",
        json={
            "name": "Iron Legion",
            "type": "order",
            "ideology": "Military discipline",
            "resources": 5000.0,
            "power_level": 80.0
        }
    )
    assert response.status_code == 201
    faction_id = response.json()["id"]

    # Read
    response = client.get(f"/api/factions/{faction_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Iron Legion"

    # Update
    response = client.put(
        f"/api/factions/{faction_id}",
        json={"power_level": 90.0}
    )
    assert response.status_code == 200
    assert response.json()["power_level"] == 90.0

    # List
    response = client.get("/api/factions/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Delete
    response = client.delete(f"/api/factions/{faction_id}")
    assert response.status_code == 204


def test_characters_crud(client):
    """Test basic CRUD operations for characters."""
    # Create
    response = client.post(
        "/api/characters/",
        json={
            "name": "Thorin Ironforge",
            "title": "Warlord",
            "role": "warrior",
            "traits": ["brave", "strategic"],
            "status": "alive"
        }
    )
    assert response.status_code == 201
    character_id = response.json()["id"]

    # Read
    response = client.get(f"/api/characters/{character_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Thorin Ironforge"
    assert "brave" in data["traits"]

    # Update
    response = client.put(
        f"/api/characters/{character_id}",
        json={"status": "missing"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "missing"

    # List with filter
    response = client.get("/api/characters/?status=missing")
    assert response.status_code == 200
    assert all(c["status"] == "missing" for c in response.json())

    # Delete
    response = client.delete(f"/api/characters/{character_id}")
    assert response.status_code == 204


def test_religions_crud(client):
    """Test basic CRUD operations for religions."""
    # Create
    response = client.post(
        "/api/religions/",
        json={
            "name": "Church of the Eternal Flame",
            "type": "deity",
            "domains": ["fire", "rebirth", "passion"],
            "description": "Worshipers of the eternal flame"
        }
    )
    assert response.status_code == 201
    religion_id = response.json()["id"]

    # Read
    response = client.get(f"/api/religions/{religion_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Church of the Eternal Flame"
    assert "fire" in data["domains"]

    # Update
    response = client.put(
        f"/api/religions/{religion_id}",
        json={"description": "Updated description"}
    )
    assert response.status_code == 200

    # List
    response = client.get("/api/religions/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Delete
    response = client.delete(f"/api/religions/{religion_id}")
    assert response.status_code == 204


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
