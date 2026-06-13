import pytest

@pytest.mark.asyncio
async def test_admin_route_protection(async_client):
    """Ensures standard users cannot access the administration matrix."""
    # 1. Register a standard user
    await async_client.post("/api/v1/auth/register", json={
        "email": "standard_user@monetlink.online",
        "password": "Password123!",
        "re_enter_password": "Password123!"
    })
    
    # 2. Login to get token
    login_resp = await async_client.post("/api/v1/auth/login", data={
        "username": "standard_user@monetlink.online",
        "password": "Password123!"
    })
    token = login_resp.json()["access_token"]
    
    # 3. Attempt to access global CPM settings endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.post("/api/v1/admin/settings/cpm", headers=headers, json={
        "country_code": "US",
        "new_rate": 50.00
    })
    
    # MUST return 403 Forbidden
    assert response.status_code == 403
    assert "insufficient privileges" in response.json()["detail"].lower()
  
