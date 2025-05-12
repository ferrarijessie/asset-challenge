import pytest
from app import db
from models import Asset, AssetType, AssetField, FieldType

@pytest.fixture
def sample_asset(app, sample_asset_type):
    """Create a sample asset for testing"""
    asset = Asset(asset_type_id=sample_asset_type.id)
    db.session.add(asset)
    db.session.commit()
    
    asset.set_value('Serial Number', 'ABC123')
    asset.set_value('Model', 'ThinkPad')
    db.session.commit()
    return asset

def test_create_asset(client, sample_asset_type):
    """Test creating a new asset"""
    data = {
        'asset_type_id': sample_asset_type.id,
        'data': {
            'Serial Number': 'XYZ789',
            'Model': 'MacBook'
        }
    }
    
    response = client.post('/api/assets/',
                         json=data)
    assert response.status_code == 201
    
    json_data = response.get_json()
    assert json_data['asset_type_id'] == sample_asset_type.id
    assert json_data['data']['Serial Number'] == 'XYZ789'
    assert json_data['data']['Model'] == 'MacBook'

def test_get_assets(client, sample_asset):
    """Test getting list of assets"""
    response = client.get('/api/assets/')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]['data']['Serial Number'] == 'ABC123'
    assert json_data[0]['data']['Model'] == 'ThinkPad'

def test_get_assets_by_type(client, sample_asset, sample_asset_type):
    """Test getting assets filtered by type"""
    response = client.get(f'/api/assets/?asset_type_id={sample_asset_type.id}')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]['asset_type_id'] == sample_asset_type.id

def test_get_asset(client, sample_asset):
    """Test getting a specific asset"""
    response = client.get(f'/api/assets/{sample_asset.id}/')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert json_data['data']['Serial Number'] == 'ABC123'
    assert json_data['data']['Model'] == 'ThinkPad'

def test_get_nonexistent_asset(client):
    """Test getting an asset that doesn't exist"""
    response = client.get('/api/assets/999/')
    assert response.status_code == 404

def test_update_asset(client, sample_asset):
    """Test updating an asset"""
    data = {
        'data': {
            'Serial Number': 'DEF456',
            'Model': 'XPS'
        }
    }
    
    response = client.put(f'/api/assets/{sample_asset.id}/',
                        json=data)
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert json_data['data']['Serial Number'] == 'DEF456'
    assert json_data['data']['Model'] == 'XPS'

def test_update_nonexistent_asset(client):
    """Test updating an asset that doesn't exist"""
    data = {
        'data': {
            'Serial Number': 'DEF456',
            'Model': 'XPS'
        }
    }
    
    response = client.put('/api/assets/999/',
                        json=data)
    assert response.status_code == 404

def test_create_asset_with_invalid_field(client, sample_asset_type):
    """Test creating an asset with an invalid field"""
    data = {
        'asset_type_id': sample_asset_type.id,
        'data': {
            'Invalid Field': 'Value'  # This field doesn't exist in the asset type
        }
    }
    
    response = client.post('/api/assets/',
                         json=data)
    assert response.status_code == 400

def test_update_asset_with_invalid_field(client, sample_asset):
    """Test updating an asset with an invalid field"""
    data = {
        'data': {
            'Invalid Field': 'Value'  # This field doesn't exist in the asset type
        }
    }
    
    response = client.put(f'/api/assets/{sample_asset.id}/',
                        json=data)
    assert response.status_code == 400
