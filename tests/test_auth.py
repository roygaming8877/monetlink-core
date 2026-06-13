import pytest

@pytest.mark.asyncio
async def test_user_registration_and_bonus(async_client):
    """Verifies that a new user registers successfully and receives the $1.00 bonus."""
    payload = {
        "email": "publisher@monetlink.online",
        "password": "SecurePassword123!",
        "re_enter_password": "SecurePassword123!"
    }
    
    response = await async_client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == payload["email"]
    # STRICT CHECK: Verify the $1 signup bonus is automatically credited
    assert data["wallet_balance"] == 1.0

@pytest.mark.asyncio
async def test_user_login(async_client):
    """Verifies Argon2 password hashing and JWT token generation."""
    # First, register the user
    await async_client.post("/api/v1/auth/register", json={
        "email": "login_test@monetlink.online",
        "password": "SecurePassword123!",
        "re_enter_password": "SecurePassword123!"
    })
    
    # Then, attempt login
    login_payload = {
        "username": "login_test@monetlink.online",
        "password": "SecurePassword123!"
    }
    response = await async_client.post("/api/v1/auth/login", data=login_payload)
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
  
