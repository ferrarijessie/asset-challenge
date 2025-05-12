#!/bin/sh

# Initialize migrations directory if it doesn't exist
if [ ! -d "migrations" ]; then
  flask db init
fi

# Always run migrations
flask db migrate -m "Auto-migration"
flask db upgrade

if [ "$1" = "test" ]; then
  pytest tests/ -v
else
  flask run --host=0.0.0.0
fi
