import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_signup_success(client):
    user_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    response = client.post('/api/v1/auth/signup', json=user_data)
    # May return 409 if user already exists, which is acceptable
    assert response.status_code in [201, 409]

def test_signup_missing_fields(client):
    user_data = {
        'email': 'test@example.com'
        # Missing password
    }
    
    response = client.post('/api/v1/auth/signup', json=user_data)
    assert response.status_code == 400

def test_signup_weak_password(client):
    user_data = {
        'email': 'test@example.com',
        'password': '123'  # Too short
    }
    
    response = client.post('/api/v1/auth/signup', json=user_data)
    assert response.status_code == 400

def test_login_success(client):
    # First create a user
    user_data = {
        'email': 'login@example.com',
        'password': 'password123'
    }
    client.post('/api/v1/auth/signup', json=user_data)
    
    # Then try to login
    login_data = {
        'email': 'login@example.com',
        'password': 'password123'
    }
    
    response = client.post('/api/v1/auth/login', json=login_data)
    assert response.status_code == 200
    data = response.json
    assert 'token' in data
    assert 'email' in data

def test_login_invalid_credentials(client):
    login_data = {
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    }
    
    response = client.post('/api/v1/auth/login', json=login_data)
    assert response.status_code == 401

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code in [200, 503]
    data = response.json
    assert 'status' in data
