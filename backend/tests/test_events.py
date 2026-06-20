import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_event(client):
    event = {
        'session_id': 'sess_123',
        'event_type': 'page_view',
        'page_url': 'https://example.com',
        'timestamp': '2024-01-01T00:00:00Z',
    }
    
    response = client.post('/api/v1/events', json=event)
    assert response.status_code == 201
    data = response.json
    assert 'event_id' in data or 'message' in data

def test_invalid_event_type(client):
    event = {
        'session_id': 'sess_123',
        'event_type': 'invalid',  # Invalid type
        'page_url': 'https://example.com',
        'timestamp': '2024-01-01T00:00:00Z',
    }
    
    response = client.post('/api/v1/events', json=event)
    assert response.status_code == 400

def test_missing_required_fields(client):
    event = {
        'session_id': 'sess_123',
        # Missing event_type, page_url, timestamp
    }
    
    response = client.post('/api/v1/events', json=event)
    assert response.status_code == 400

def test_list_events(client):
    response = client.get('/api/v1/events')
    assert response.status_code == 200
    data = response.json
    assert 'data' in data or 'events' in data
