from flask_restx import Api, fields

# Initialize API
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY',
        'description': 'API Key for authorization'
    }
}

api = Api(
    title='Asset Management API',
    version='1.0',
    description='A RESTful API for managing different types of assets with flexible schemas',
    authorizations=authorizations,
    security='apikey',  # This makes all endpoints require the API key by default
    doc='/docs'
)

# API models/schemas
asset_field = api.model('AssetField', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True, description='Field name'),
    'field_type': fields.String(required=True, enum=['text', 'number'], description='Field type', attribute=lambda x: x.field_type.value if x.field_type else None)
})

asset_field_input = api.model('AssetFieldInput', {
    'name': fields.String(required=True, description='Field name'),
    'field_type': fields.String(required=True, enum=['text', 'number'], description='Field type', attribute=lambda x: x.field_type.value if x.field_type else None)
})

asset_type = api.model('AssetType', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True, description='Asset type name'),
    'fields': fields.List(fields.Nested(asset_field))
})

asset_type_input = api.model('AssetTypeInput', {
    'name': fields.String(required=True, description='Asset type name'),
    'fields': fields.List(fields.Nested(asset_field_input), required=True)
})

asset_data = api.model('AssetData', {
    'asset_type_id': fields.Integer(required=True),
    'data': fields.Raw(required=True)
})

asset = api.model('Asset', {
    'id': fields.Integer(readonly=True),
    'asset_type_id': fields.Integer(),
    'data': fields.Raw(attribute=lambda x: x.get_all_fields_with_values())
})

# API namespaces
asset_ns = api.namespace('api/asset-types', description='Asset type operations')
assets_ns = api.namespace('api/assets', description='Asset operations')
