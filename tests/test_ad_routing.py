import pytest

@pytest.mark.asyncio
async def test_multi_step_ad_routing(async_client):
    """Simulates the user traversing the Captcha -> Article -> Final Counter flow."""
    # Create a link first
    await async_client.post("/api/v1/links/shorten", json={
        "original_url": "https://target-destination.com",
        "alias": "ad-flow-test"
    })
    
    # Step 1: Hit the short link directly (Should return Captcha Template)
    step1_response = await async_client.get("/ad-flow-test")
    assert step1_response.status_code == 200
    assert "step1_captcha.html" in step1_response.text or "captcha" in step1_response.text.lower()
    
    # Step 2: Simulate clearing Captcha, route to Article
    step2_response = await async_client.get("/validate/step1/ad-flow-test")
    assert step2_response.status_code == 200
    assert "step2_article.html" in step2_response.text or "article" in step2_response.text.lower()

    # Step 3: Simulate 10-second timer completion, route to final destination
    step3_response = await async_client.get("/go/ad-flow-test", follow_redirects=False)
    # Should be a 302/307 Redirect to the actual destination
    assert step3_response.status_code in [302, 307]
    assert step3_response.headers["location"] == "https://target-destination.com"
  
