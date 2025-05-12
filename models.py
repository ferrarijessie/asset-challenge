from app import db
from datetime import datetime
from enum import Enum

class FieldType(str, Enum):
    TEXT = 'text'
    NUMBER = 'number'

# Association table for AssetType and AssetField
asset_type_fields = db.Table('asset_type_fields',
    db.Column('asset_type_id', db.Integer, db.ForeignKey('asset_types.id'), primary_key=True),
    db.Column('asset_field_id', db.Integer, db.ForeignKey('asset_fields.id'), primary_key=True)
)

class AssetField(db.Model):
    __tablename__ = 'asset_fields'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    field_type = db.Column(db.Enum(FieldType), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Add unique constraint to prevent duplicate field names
    __table_args__ = (db.UniqueConstraint('name', name='uq_asset_field_name'),)

    def __str__(self):
        return self.field_type.value

class AssetType(db.Model):
    __tablename__ = 'asset_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Many-to-many relationship with AssetField
    fields = db.relationship('AssetField', secondary=asset_type_fields,
                           backref=db.backref('asset_types', lazy=True))

class AssetValue(db.Model):
    __tablename__ = 'asset_values'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('asset_fields.id'), nullable=False)
    text_value = db.Column(db.String)
    number_value = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    field = db.relationship('AssetField')
    
    # Ensure we don't have duplicate field values for the same asset
    __table_args__ = (db.UniqueConstraint('asset_id', 'field_id', name='uq_asset_field_value'),)

    def get_value(self):
        """Get the value based on field type"""
        return self.text_value if self.field.field_type == FieldType.TEXT else self.number_value

class Asset(db.Model):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_type_id = db.Column(db.Integer, db.ForeignKey('asset_types.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    asset_type = db.relationship('AssetType', backref=db.backref('assets', lazy=True))
    values = db.relationship('AssetValue', backref='asset', cascade='all, delete-orphan')
    
    def get_value(self, field_name):
        """Get the value of a specific field by name"""
        for value in self.values:
            if value.field.name == field_name:
                return value.text_value if value.field.field_type == FieldType.TEXT else value.number_value
        return None
        
    def get_all_fields_with_values(self):
        """Get all fields from the asset type with their current values"""
        result = {}
        # First, add all fields with None values
        for field in self.asset_type.fields:
            result[field.name] = None
        # Then, update with actual values where they exist
        for value in self.values:
            result[value.field.name] = value.get_value()
        return result
    
    def set_value(self, field_name, value):
        """Set the value for a specific field by name"""
        # Find the field in the asset type's fields
        field = next((f for f in self.asset_type.fields if f.name == field_name), None)
        if not field:
            raise ValueError(f"Field {field_name} is not defined for this asset type")
        
        # Find or create the asset value
        asset_value = next((av for av in self.values if av.field.name == field_name), None)
        if not asset_value:
            asset_value = AssetValue(asset=self, field=field)
            self.values.append(asset_value)
        
        # Set the appropriate value based on field type
        if field.field_type == FieldType.TEXT:
            asset_value.text_value = str(value)
            asset_value.number_value = None
        else:  # NUMBER
            try:
                asset_value.number_value = float(value)
                asset_value.text_value = None
            except (ValueError, TypeError):
                raise ValueError(f"Invalid number value for field {field_name}")
