import pytest
import httpx
from app.main import app

# Use pytest-asyncio for async tests
@pytest.mark.asyncio
async def test_create_user_profile():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post(
            "/users", 
            json={"username": "test_user", "email": "test@example.com", "password": "password123"}
        )
    
    assert response.status_code == 201
    # Uncomment and modify this if you want to check the response
    # assert response.json() == {"username": "test_user", "email": "testasd@example.com"}

# Test to get a user (user found)
@pytest.mark.asyncio
async def test_get_user_profile():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/users/test@example.com")
    
    assert response.status_code == 200
    assert response.json() == {"username": "test_user", "email": "test@example.com"}

# Test to get a user (user not found)
@pytest.mark.asyncio
async def test_get_user_profile_not_found():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/users/test@example.com")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "User with ID test@example.com not found"}

# Test to update a user (user found)
@pytest.mark.asyncio
async def test_update_user_profile():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.put(
            "/users/test@example.com", 
            json={"username": "updated_user", "email": "updated@example.com"}
        )
    
    assert response.status_code == 200
    assert response.json() == {"id": "123", "username": "updated_user", "email": "updated@example.com"}

# Test to update a user (user not found)
@pytest.mark.asyncio
async def test_update_user_profile_not_found():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.put(
            "/users/test@example.com", 
            json={"username": "updated_user", "email": "updated@example.com"}
        )
    
    assert response.status_code == 404
    assert response.json() == {"detail": "User with email test@example.com not found"}

# Test to delete a user (user found)
@pytest.mark.asyncio
async def test_delete_user_profile():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.delete("/users/test@example.com")
    
    assert response.status_code == 204
    assert response.content == b""

# Test to delete a user (user not found)
@pytest.mark.asyncio
async def test_delete_user_profile_not_found():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.delete("/users/test@example.com")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "User with ID test@example.com not found"}
