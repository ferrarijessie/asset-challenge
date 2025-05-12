# Asset Management API

A RESTful API built with Flask and PostgreSQL for managing different types of assets with flexible schemas.

## Features

- Dynamic asset types with customizable schemas
- CRUD operations for assets
- PostgreSQL database with JSONB support
- Docker and Docker Compose setup

## Database Schema Design

The application uses a flexible schema design to support different types of assets with varying fields:

### Core Entities

1. **Asset Fields** (`asset_fields` table)
   - Reusable field definitions with name and type (Text/Number)
   - Can be shared across multiple asset types
   - Fields: id, name, field_type, created_at, updated_at

2. **Asset Types** (`asset_types` table)
   - Templates that define what fields an asset can have
   - Many-to-many relationship with Asset Fields
   - Fields: id, name, created_at, updated_at

3. **Assets** (`assets` table)
   - Concrete instances of asset types
   - Each asset belongs to one asset type
   - Fields: id, asset_type_id, created_at, updated_at

4. **Asset Values** (`asset_values` table)
   - Stores the actual values for each field of an asset
   - Supports different value types (text_value, number_value)
   - Fields: id, asset_id, field_id, text_value, number_value, created_at, updated_at

### Key Design Decisions

1. **Flexible Field Types**
   Instead of using JSONB, I opted for a structured approach with separate columns for different value types which enable better type validation and querying capabilities.

2. **Many-to-Many Relationships**
   Asset Fields can be shared across multiple Asset Types using the `asset_type_fields` junction table. Reducing duplication and allowing field reuse.

3. **Separate Value Storage**
   Asset values are stored in a separate table rather than as JSON. This provides better data integrity and validation. Makes it easier to manipulate values and display them in any structure desired.

## Getting Started

1. Clone the repository
2. Make sure you have Docker and Docker Compose installed
3. Run the application:

```
docker-compose up --build
```

The API will be available at `http://localhost:5065`

API documentation (Swagger UI) is available at `http://localhost:5065/docs`

## Database Management

The application uses Flask-Migrate (Alembic) for database migrations. Migrations are automatically handled when the container starts up, but you can also run them manually:

### Initialize Migrations (First Time Setup)
```
docker-compose exec api flask db init
```

### Create a New Migration
```
docker-compose exec api flask db migrate -m "Description of changes"
```

### Apply Migrations
```
docker-compose exec api flask db upgrade
```

### View Migration Status
```
docker-compose exec api flask db current
```

Note: The application automatically runs pending migrations on startup. You only need to run these commands manually if you want to create new migrations or check the migration status.

## Design Choices and Assumptions

### Architecture

1. **Service Layer Pattern (MVC)**
   All database operations are centralized in service classes, keeping the routes focused on HTTP concerns. This makes the codebase more maintainable and easier to test.

2. **API Key Authentication**
   Simple API key authentication is implemented as a proof of concept. In a production environment, this should be replaced with more robust authentication (e.g., JWT, OAuth).

### API Design

1. **RESTful Conventions**
   - Resources are noun-based (`/assets`, `/asset-types`)
   - HTTP methods indicate actions (GET, POST, PUT)
   - Nested resources use parent IDs (`/asset-types/{id}/fields`)

2. **Response Structure**
   - Consistent error responses with appropriate HTTP status codes
   - Asset fields and values are returned in a flexible `data` object even if the field doesn't have a value set, this is to allow for easy updates and to avoid missing fields when updating an asset.

### Assumptions

1. **Field Types**
   - Limited to text and number types for simplicity
   - Additional types (date, boolean, etc.) could be added following the same pattern

2. **Validation**
   - Field names must be unique within an asset type
   - Asset values must match their field's type
   - Assets cannot change their type after creation to avoid data integrity issues.

3. **Performance**
   - The current design assumes a moderate scale of assets and types
   - For very large datasets, additional optimizations would be needed (caching, indexing)

## AI-Assisted Development

This project was developed with the assistance of Cascade, an AI coding assistant. 

The AI assistant served as a pair programmer, offering suggestions and improvements while ensuring the code followed best practices and maintained high quality standards.

## API Endpoints

### Asset Types
- `POST /api/asset-types` - Create a new asset type
- `GET /api/asset-types` - List all asset types
- `GET /api/asset-types/<id>` - Get a specific asset type

### Asset Types Fields
- `POST /api/asset-types/<id>/fields` - Add a field to an asset type
- `GET /api/asset-types/<id>/fields` - Get fields for an asset type

### Assets
- `POST /api/assets` - Create a new asset
- `GET /api/assets` - List all assets (can filter by asset_type_id)
- `GET /api/assets/<id>` - Get a specific asset
- `PUT /api/assets/<id>` - Update an asset

## Example Usage

1. Create an asset type:
```json
POST /api/asset-types
{
    "name": "laptop",
    "fields": [
        {"name": "brand", "field_type": "text"},
        {"name": "model", "field_type": "text"},
        {"name": "purchase_date", "field_type": "text"}
    ]
}
```

2. Create an asset:
```json
POST /api/assets
{
    "asset_type_id": 1,
    "data": {
        "brand": "Dell",
        "model": "XPS 13",
        "purchase_date": "2025-01-15"
    }
}
```

## Running Tests

The project includes automated tests that can be run using Docker Compose:

```
docker-compose run test
```

This will run all tests in an isolated environment using an in-memory SQLite database.