import pytest
from app import app as flask_app, db
from models import AssetType, AssetField, FieldType

@pytest.fixture
def app():
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['TESTING'] = True
    
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    test_client = app.test_client()
    test_client.environ_base['HTTP_X_API_KEY'] = 'Dyn4m1cAsS3tKey'
    return test_client

@pytest.fixture
def sample_asset_type(app):
    with app.app_context():
        # Create fields
        serial_field = AssetField(name='Serial Number', field_type=FieldType.TEXT)
        model_field = AssetField(name='Model', field_type=FieldType.TEXT)
        db.session.add_all([serial_field, model_field])
        
        # Create asset type with fields
        asset_type = AssetType(name='Laptop')
        asset_type.fields.extend([serial_field, model_field])
        db.session.add(asset_type)
        db.session.commit()
        
        # Get a fresh instance that's attached to the session
        asset_type_id = asset_type.id
        return db.session.get(AssetType, asset_type_id)
