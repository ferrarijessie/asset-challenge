import pytest
import json
from models import AssetType, AssetField

def test_create_asset_type(client):
    """Test creating a new asset type with fields"""
    data = {
        'name': 'Monitor',
        'fields': [
            {'name': 'Serial Number', 'field_type': 'text'},
            {'name': 'Screen Size', 'field_type': 'number'}
        ]
    }
    
    response = client.post('/api/asset-types/',
                         json=data)
    assert response.status_code == 201
    
    # Check response data
    json_data = response.get_json()
    assert json_data['name'] == 'Monitor'
    assert len(json_data['fields']) == 2
    
    # Verify field names and types
    field_names = {f['name'] for f in json_data['fields']}
    assert 'Serial Number' in field_names
    assert 'Screen Size' in field_names

def test_get_asset_types(client, sample_asset_type):
    """Test getting list of asset types"""
    response = client.get('/api/asset-types/')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]['name'] == 'Laptop'
    assert len(json_data[0]['fields']) == 2

def test_get_asset_type(client, sample_asset_type):
    """Test getting a single asset type by ID"""
    response = client.get(f'/api/asset-types/{sample_asset_type.id}/')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert json_data['name'] == 'Laptop'
    assert len(json_data['fields']) == 2
    
    # Check that fields are correctly returned
    field_names = {f['name'] for f in json_data['fields']}
    assert 'Serial Number' in field_names
    assert 'Model' in field_names

def test_get_nonexistent_asset_type(client):
    """Test getting an asset type that doesn't exist"""
    response = client.get('/api/asset-types/999/')
    assert response.status_code == 404

def test_create_field_for_asset_type(client, sample_asset_type):
    """Test adding a new field to an existing asset type"""
    data = {
        'name': 'Purchase Date',
        'field_type': 'text'
    }
    
    response = client.post(f'/api/asset-types/{sample_asset_type.id}/fields/',
                         json=data)
    assert response.status_code == 201
    
    # Verify the field was added
    json_data = response.get_json()
    assert json_data['name'] == 'Purchase Date'
    assert json_data['field_type'] == 'text'

def test_get_asset_type_fields(client, sample_asset_type):
    """Test getting fields for an asset type"""
    response = client.get(f'/api/asset-types/{sample_asset_type.id}/fields/')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert len(json_data) == 2
    
    # Verify field names
    field_names = {f['name'] for f in json_data}
    assert 'Serial Number' in field_names
    assert 'Model' in field_names

def test_create_duplicate_field(client, sample_asset_type):
    """Test adding a field that already exists for the asset type"""
    data = {
        'name': 'Serial Number',  # This field already exists
        'field_type': 'text'
    }
    
    response = client.post(f'/api/asset-types/{sample_asset_type.id}/fields/',
                         json=data)
    assert response.status_code == 400
    
    json_data = response.get_json()
    assert 'message' in json_data
