import pytest

@pytest.mark.asyncio
async def test_create_short_link(async_client):
    """Verifies the API accurately generates a shortened URL matrix."""
    payload = {
        "original_url": "https://www.example.com/massive-download-file",
        "alias": "custom-alias-123"
    }
    
    response = await async_client.post("/api/v1/links/shorten", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["original_url"] == payload["original_url"]
    assert data["alias"] == payload["alias"]
    assert "monetlink.online" in data["shortened_url"]

@pytest.mark.asyncio
async def test_duplicate_alias_rejection(async_client):
    """Verifies system blocks users from claiming already taken aliases."""
    payload = {"original_url": "https://example.com", "alias": "premium-link"}
    
    await async_client.post("/api/v1/links/shorten", json=payload)
    response2 = await async_client.post("/api/v1/links/shorten", json=payload)
    
    # Must throw a 400 Bad Request for duplicate alias
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"].lower()
  
