"""Tests for Locations API endpoints."""
import pytest


def test_create_location(client):
    """Test creating a location via API."""
    response = client.post(
        "/api/locations/",
        json={
            "name": "Dragonspire",
            "type": "mountain",
            "short_description": "A volcanic mountain",
            "tags": ["volcanic", "dangerous"]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Dragonspire"
    assert data["type"] == "mountain"
    assert "volcanic" in data["tags"]
    assert "id" in data


def test_get_locations(client):
    """Test getting list of locations."""
    # Create some locations
    client.post("/api/locations/", json={"name": "City A", "type": "city"})
    client.post("/api/locations/", json={"name": "Village B", "type": "village"})

    # Get all locations
    response = client.get("/api/locations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_get_location_by_id(client):
    """Test getting a specific location by ID."""
    # Create a location
    create_response = client.post(
        "/api/locations/",
        json={"name": "Test City", "type": "city"}
    )
    location_id = create_response.json()["id"]

    # Get the location
    response = client.get(f"/api/locations/{location_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test City"
    assert data["id"] == location_id


def test_get_nonexistent_location(client):
    """Test getting a location that doesn't exist."""
    response = client.get("/api/locations/99999")
    assert response.status_code == 404


def test_update_location(client):
    """Test updating a location."""
    # Create a location
    create_response = client.post(
        "/api/locations/",
        json={"name": "Old Name", "type": "city"}
    )
    location_id = create_response.json()["id"]

    # Update it
    response = client.put(
        f"/api/locations/{location_id}",
        json={"name": "New Name", "short_description": "Updated"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["short_description"] == "Updated"


def test_delete_location(client):
    """Test deleting a location."""
    # Create a location
    create_response = client.post(
        "/api/locations/",
        json={"name": "To Delete", "type": "ruins"}
    )
    location_id = create_response.json()["id"]

    # Delete it
    response = client.delete(f"/api/locations/{location_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/locations/{location_id}")
    assert response.status_code == 404


def test_filter_locations_by_type(client):
    """Test filtering locations by type."""
    client.post("/api/locations/", json={"name": "City 1", "type": "city"})
    client.post("/api/locations/", json={"name": "Village 1", "type": "village"})

    response = client.get("/api/locations/?location_type=city")
    assert response.status_code == 200
    data = response.json()
    assert all(loc["type"] == "city" for loc in data)


def test_search_locations(client):
    """Test searching locations."""
    client.post(
        "/api/locations/",
        json={"name": "Mystic Forest", "type": "forest", "short_description": "magical woods"}
    )

    response = client.get("/api/locations/?search=Mystic")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any("Mystic" in loc["name"] for loc in data)
