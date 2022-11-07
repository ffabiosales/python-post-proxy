from aiohttp import web
from  src.main import app_factory, index, JWT_SECRET
import pytest
# import jwt

@pytest.mark.asyncio
async def test_post(aiohttp_client):

    app = web.Application()
    app.router.add_post("/", index)
    client = await aiohttp_client(app)

    payload = {"test_data": "test_value"}

    resp = await client.post("/", headers={"content-type": "application/json"}, json=payload)    
    data = await resp.json()
    assert resp.status == 200
    assert data["data"] == "test_data=test_value"
    assert "x-my-jwt" in data["headers"].keys()