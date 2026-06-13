import pytest

@pytest.mark.asyncio
async def test_ip_based_fraud_limiter(async_client):
    """Validates that rapid successive clicks from the same IP are marked invalid."""
    # Setup short link
    await async_client.post("/api/v1/links/shorten", json={
        "original_url": "https://example.com",
        "alias": "fraud-check-link"
    })
    
    # Simulate headers from the same IP Address
    headers = {"X-Forwarded-For": "192.168.1.100"}
    
    # First Click (Should process normally and credit payout)
    resp1 = await async_client.get("/go/fraud-check-link", headers=headers, follow_redirects=False)
    assert resp1.status_code in [302, 307]
    
    # Second Click immediately from same IP (Should trigger rate limiter / fraud block)
    resp2 = await async_client.get("/go/fraud-check-link", headers=headers, follow_redirects=False)
    # Depending on configuration, it either redirects but doesn't credit, or throws 429
    assert resp2.status_code == 429
    assert "too many requests" in resp2.json()["detail"].lower()
  
