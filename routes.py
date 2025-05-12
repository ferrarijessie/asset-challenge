from flask import request
from flask_restx import Resource
from app import require_api_key
from models import FieldType
from service import AssetTypeService, AssetService
from api import (
    api, asset_ns, assets_ns,
    asset_type, asset_type_input,
    asset_field, asset_field_input,
    asset, asset_data
)

@asset_ns.route('/')
class AssetTypeList(Resource):
    method_decorators = [require_api_key]
    @asset_ns.doc('list_asset_types')
    @asset_ns.marshal_list_with(asset_type)
    def get(self):
        """List all asset types"""
        return AssetTypeService.get_all_asset_types()

    @asset_ns.doc('create_asset_type')
    @asset_ns.expect(asset_type_input)
    @asset_ns.response(201, 'Asset type created successfully')
    @asset_ns.marshal_with(asset_type, code=201)
    def post(self):
        """Create a new asset type"""
        data = api.payload
        new_asset_type = AssetTypeService.create_asset_type(
            name=data['name'],
            fields_data=data['fields']
        )
        return new_asset_type, 201

@asset_ns.route('/<int:type_id>/')
class AssetTypeItem(Resource):
    method_decorators = [require_api_key]
    @asset_ns.doc('get_asset_type')
    @asset_ns.marshal_with(asset_type)
    def get(self, type_id):
        """Get a specific asset type"""
        return AssetTypeService.get_asset_type(type_id)

@asset_ns.route('/<int:type_id>/fields/')
class AssetTypeFields(Resource):
    method_decorators = [require_api_key]
    @asset_ns.doc('get_asset_type_fields')
    @asset_ns.marshal_list_with(asset_field)
    def get(self, type_id):
        """Get fields for an asset type"""
        return AssetTypeService.get_asset_type_fields(type_id)

    @asset_ns.doc('add_field_to_asset_type')
    @asset_ns.expect(asset_field_input)
    @asset_ns.response(201, 'Field added successfully')
    @asset_ns.marshal_with(asset_field, code=201)
    def post(self, type_id):
        """Add a field to an asset type"""
        data = api.payload
        try:
            field = AssetTypeService.add_field_to_asset_type(
                type_id=type_id,
                field_name=data['name'],
                field_type=FieldType(data['field_type'])
            )
            return field, 201
        except ValueError as e:
            api.abort(400, str(e))

@assets_ns.route('/')
class AssetList(Resource):
    method_decorators = [require_api_key]
    @assets_ns.doc('list_assets')
    @assets_ns.marshal_list_with(asset)
    def get(self):
        """List all assets"""
        asset_type_id = request.args.get('asset_type_id', type=int)
        return AssetService.get_all_assets(asset_type_id)

    @assets_ns.doc('create_asset')
    @assets_ns.expect(asset_data)
    @assets_ns.response(201, 'Asset created successfully')
    @assets_ns.marshal_with(asset, code=201)
    def post(self):
        """Create a new asset"""
        data = api.payload
        try:
            new_asset = AssetService.create_asset(
                asset_type_id=data['asset_type_id'],
                field_values=data['data']
            )
            return new_asset, 201
        except ValueError as e:
            api.abort(400, str(e))

@assets_ns.route('/<int:asset_id>/')
class AssetItem(Resource):
    method_decorators = [require_api_key]
    @assets_ns.doc('get_asset')
    @assets_ns.marshal_with(asset)
    def get(self, asset_id):
        """Get a specific asset"""
        return AssetService.get_asset(asset_id)

    @assets_ns.doc('update_asset')
    @assets_ns.expect(asset_data)
    @assets_ns.marshal_with(asset)
    def put(self, asset_id):
        """Update an asset"""
        data = api.payload
        try:
            updated_asset = AssetService.update_asset(
                asset_id=asset_id,
                field_values=data['data']
            )
            return updated_asset
        except ValueError as e:
            api.abort(400, str(e))
