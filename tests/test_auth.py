import pytest

def test_missing_api_key(app):
    """Test that requests without API key are rejected"""
    client = app.test_client()
    response = client.get('/api/asset-types/')
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Unauthorized'

def test_invalid_api_key(app):
    """Test that requests with invalid API key are rejected"""
    client = app.test_client()
    headers = {'X-API-KEY': 'invalid_key'}
    response = client.get('/api/asset-types/', headers=headers)
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Unauthorized'

def test_valid_api_key(app):
    """Test that requests with valid API key are accepted"""
    client = app.test_client()
    headers = {'X-API-KEY': 'Dyn4m1cAsS3tKey'}
    response = client.get('/api/asset-types/', headers=headers)
    assert response.status_code == 200
