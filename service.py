from app import db
from models import AssetType, Asset, AssetField, FieldType

class AssetTypeService:
    @staticmethod
    def get_all_asset_types():
        """Get all asset types"""
        return AssetType.query.all()
    
    @staticmethod
    def get_asset_type(type_id):
        """Get a specific asset type by ID"""
        return AssetType.query.get_or_404(type_id)
    
    @staticmethod
    def create_asset_type(name, fields_data):
        """Create a new asset type with fields"""
        new_asset_type = AssetType(name=name)
        db.session.add(new_asset_type)
        
        # Create and associate fields
        for field_data in fields_data:
            field = AssetField.query.filter_by(name=field_data['name']).first()
            if not field:
                field = AssetField(
                    name=field_data['name'],
                    field_type=FieldType(field_data['field_type'])
                )
                db.session.add(field)
            new_asset_type.fields.append(field)
        
        db.session.commit()
        return new_asset_type
    
    @staticmethod
    def add_field_to_asset_type(type_id, field_name, field_type):
        """Add a field to an asset type"""
        asset_type = AssetType.query.get_or_404(type_id)
        
        # Check if field already exists for this asset type
        if any(f.name == field_name for f in asset_type.fields):
            raise ValueError(f"Field {field_name} already exists for this asset type")
        
        field = AssetField.query.filter_by(name=field_name).first()
        if not field:
            field = AssetField(
                name=field_name,
                field_type=field_type
            )
            db.session.add(field)
        
        asset_type.fields.append(field)
        db.session.commit()
        return field
    
    @staticmethod
    def get_asset_type_fields(type_id):
        """Get all fields for an asset type"""
        asset_type = AssetType.query.get_or_404(type_id)
        return asset_type.fields


class AssetService:
    @staticmethod
    def get_all_assets(asset_type_id=None):
        """Get all assets, optionally filtered by asset type"""
        query = Asset.query
        if asset_type_id:
            query = query.filter_by(asset_type_id=asset_type_id)
        return query.all()
    
    @staticmethod
    def get_asset(asset_id):
        """Get a specific asset by ID"""
        return Asset.query.get_or_404(asset_id)
    
    @staticmethod
    def create_asset(asset_type_id, field_values):
        """Create a new asset with field values"""
        # Create new asset
        new_asset = Asset(asset_type_id=asset_type_id)
        db.session.add(new_asset)
        db.session.commit()
        
        try:
            # Set field values
            for field_name, value in field_values.items():
                try:
                    new_asset.set_value(field_name, value)
                except ValueError as e:
                    db.session.delete(new_asset)
                    db.session.commit()
                    raise ValueError(str(e))
            
            db.session.commit()
            return new_asset
        except Exception as e:
            db.session.delete(new_asset)
            db.session.commit()
            raise
    
    @staticmethod
    def update_asset(asset_id, field_values):
        """Update an asset's field values"""
        asset = Asset.query.get_or_404(asset_id)
        
        try:
            # Update field values
            for field_name, value in field_values.items():
                try:
                    asset.set_value(field_name, value)
                except ValueError as e:
                    db.session.rollback()
                    raise ValueError(str(e))
            
            db.session.commit()
            return asset
        except Exception as e:
            db.session.rollback()
            raise
