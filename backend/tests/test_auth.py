def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={"email": "testuser@test.com", "password": "testtest"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@test.com"

def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={"email": "testuser@test.com", "password": "testtest"}
    )
    response = client.post(
        "/auth/register",
        json={"email": "testuser@test.com", "password": "testtest"}
    )
    assert response.status_code == 400

def test_login_success(client):
    client.post(
        "/auth/register",
        json={"email": "testuser@test.com", "password": "testtest"}
    )
    response = client.post(
        "/auth/login",
        json={"email": "testuser@test.com", "password": "testtest"}
    )
    assert "access_token" in response.json()    
    assert response.json()["token_type"] == "bearer"

def test_login_failure(client):    
    response = client.post(
        "/auth/login",
        json={"email": "testuser@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401